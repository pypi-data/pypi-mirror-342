import torch
import json
import numpy as np
from special_attentions.utils.mask_related import calc_attn_block_sum_efficient
from special_attentions.utils.block_sparse_attn_kernel import sparse_attention_factory
from special_attentions.utils.tools import preserve_rng_state, timeit
from special_attentions.utils.gilbert3d import gilbert3d
from colorama import Fore, Style
def concentrated_interpolation(min_val, max_val, n_points, concentration=0.2):
    """
    生成集中在最小值和最大值附近的插值点。

    Args:
        min_val (float): 最小值
        max_val (float): 最大值
        n_points (int): 插值点数量
        concentration (float): 集中度控制（0-1，越高越集中）

    Returns:
        np.ndarray: 插值点数组
    """
    concentration = np.clip(concentration, 0.05, 0.95)
    x = np.linspace(-6, 6, n_points)
    scale = 2 * (1 - concentration)
    cdf = 1 / (1 + np.exp(-x / scale))
    interpolated = max_val - cdf * (max_val - min_val)
    return np.clip(interpolated, min_val, max_val)

def transfer_attn_to_mask(attn, mode="energy", init_k=None, max_retain_ratio=0.7, min_retain_ratio=0.1, energy_threshold=0.95):
    """
    将注意力权重转换为掩码矩阵。

    Args:
        attn (torch.Tensor): 注意力权重矩阵，形状为 [batch, head, seq, seq]
        mode (str): 掩码生成模式，支持 "topk" 或 "energy"
        init_k (float, optional): topk 模式下的初始 k 值
        max_retain_ratio (float): energy 模式下的最大保留比例
        min_retain_ratio (float): energy 模式下的最小保留比例
        energy_threshold (float): energy 模式下的能量阈值

    Returns:
        torch.Tensor: 二值掩码矩阵，形状同输入
    """
    batch, heads, seq, _ = attn.shape
    device = attn.device
    mask = torch.zeros_like(attn, dtype=torch.bool)

    if mode == "topk":
        if init_k is None:
            raise ValueError("在 topk 模式下必须提供 init_k")
        init_k = int(seq * init_k) if init_k < 1 else int(init_k)
        sorted_attn, indices = torch.sort(attn, dim=-1, descending=True)
        cum_energy = torch.cumsum(sorted_attn, dim=-1)
        total_energy = cum_energy[..., -1:]
        current_k = torch.full((batch, heads, seq), init_k, device=device, dtype=torch.int64)

        current_energy = cum_energy.gather(dim=-1, index=(current_k - 1).unsqueeze(-1)).squeeze(-1)
        condition_met = current_energy >= (0.6 * total_energy.squeeze(-1))
        condition_met1 = current_energy >= (0.9 * total_energy.squeeze(-1))

        need_update = (~condition_met) & (current_k < seq)
        need_update1 = (~condition_met1) & (current_k < seq)
        current_k[need_update] = torch.clamp(current_k[need_update] * 3, max=seq)
        current_k[need_update1] = torch.clamp(current_k[need_update1] // 3 * 2, max=seq)

        pos_indices = torch.arange(seq, device=device).view(1, 1, 1, seq)
        keep_mask = pos_indices < current_k.unsqueeze(-1)
        mask.scatter_(-1, indices, keep_mask)

    elif mode == "energy":
        min_retain = max(1, int(seq * min_retain_ratio))
        max_retain = max(1, int(seq * max_retain_ratio))
        sorted_attn, indices = torch.sort(attn, dim=-1, descending=True)
        cum_energy = torch.cumsum(sorted_attn, dim=-1)
        total_energy = cum_energy[..., -1:]

        energy_mask = cum_energy >= energy_threshold * total_energy
        k_indices = torch.argmax(energy_mask.int(), dim=-1)
        unsatisfied = (cum_energy[..., -1:] < energy_threshold * total_energy).squeeze(-1)
        k_indices = torch.where(unsatisfied, seq, k_indices)
        k_indices = torch.clamp(k_indices, min=min_retain, max=max_retain)

        pos_indices = torch.arange(seq, device=device).view(1, 1, 1, seq)
        keep_mask = pos_indices < k_indices.unsqueeze(-1)
        mask.scatter_(-1, indices, keep_mask)

    else:
        raise ValueError(f"不支持的模式: {mode}")

    mask[:, :, -2:] = True
    mask[:, :, :, -2:] = True
    return mask

class GilbertRearranger:
    """基于 Gilbert 曲线的序列重排器，用于视频和文本数据的重新排列。"""
    def __init__(self, width, height, depth, text_length=224):
        self.width = width
        self.height = height
        self.depth = depth
        self.total_elements = width * height * depth
        self.text_length = text_length

        coord_to_index = self._gilbert3d_with_index(width, height, depth)
        original_order2gilbert_order = [0] * self.total_elements
        gilbert_order2original_order = [0] * self.total_elements

        for coord_idx, org_idx in coord_to_index.items():
            original_order2gilbert_order[org_idx] = coord_idx
            gilbert_order2original_order[coord_idx] = org_idx

        self.original_order2gilbert_order = torch.tensor(original_order2gilbert_order, dtype=torch.long, device='cuda')
        self.gilbert_order2original_order = torch.tensor(gilbert_order2original_order, dtype=torch.long, device='cuda')

    def _gilbert3d_with_index(self, width, height, depth):
        """生成 Gilbert 曲线的坐标到索引映射。"""
        coord_to_index = {}
        index = 0
        def coord_to_index_func(x, y, z):
            return x + width * (y + height * z)
        for x, y, z in gilbert3d(width, height, depth):
            coord_index = coord_to_index_func(x, y, z)
            coord_to_index[coord_index] = index
            index += 1
        return coord_to_index

    def rearrange(self, q, k, v):
        """将 q、k、v 张量的视频部分按 Gilbert 曲线顺序重排。"""
        seq_dim = -2
        text_part_q, video_part_q = q[..., :self.text_length, :], q[..., self.text_length:, :]
        text_part_k, video_part_k = k[..., :self.text_length, :], k[..., self.text_length:, :]
        text_part_v, video_part_v = v[..., :self.text_length, :], v[..., self.text_length:, :]

        q_rearranged = video_part_q.index_select(seq_dim, self.original_order2gilbert_order)
        k_rearranged = video_part_k.index_select(seq_dim, self.original_order2gilbert_order)
        v_rearranged = video_part_v.index_select(seq_dim, self.original_order2gilbert_order)

        return (torch.cat((q_rearranged,text_part_q), dim=seq_dim),
                torch.cat((k_rearranged,text_part_k), dim=seq_dim),
                torch.cat((v_rearranged,text_part_v), dim=seq_dim))

    def reversed_rearrange(self, out):
        """将输出张量的视频部分从 Gilbert 曲线顺序恢复到原始顺序。"""
        seq_dim = -2
        video_part,text_part= out[..., :-self.text_length, :], out[..., -self.text_length:, :]
        out_reversed = video_part.index_select(seq_dim, self.gilbert_order2original_order)
        return torch.cat((text_part, out_reversed), dim=seq_dim)

class BlockSparseAttention:
    """块稀疏注意力模块，支持动态掩码生成和稀疏度记录。"""
    def __init__(self, block_size=64, layernum=42, timestep=50, num_samples=1, warmup_epoch=5):
        self.block_size = block_size
        self.layernum = layernum
        self.timestep = timestep
        self.num_samples = num_samples
        self.warmup_epoch = warmup_epoch
        self.counter = 0

        self.sparsity_records = [self._init_sparsity_dict() for _ in range(num_samples)]
        self.update_list = [0, 1, 2, 3, 4, 5, 10, 15, 25, 35, 45, 48]
        self.mask = [None] * layernum
        self.k_list = [0.3, 0.2, 0.15, 0.1]
        self.max_retain_ratio_list = concentrated_interpolation(0.93, 0.98, 50, concentration=0.3)
        self.min_retain_ratio_list = concentrated_interpolation(0.10, 0.12, 50, concentration=0.5)
        self.energy_threshold_list = concentrated_interpolation(0.93, 0.99, 50, concentration=0.5)

        self.block_sparse_triton_fn = sparse_attention_factory(block_size, block_size)
        self.rearranger = GilbertRearranger(width=85, height=48, depth=11, text_length=224)

    def _init_sparsity_dict(self):
        """初始化稀疏度记录字典。"""
        return {"records": []}

    def _calculate_sparsity(self, mask):
        """计算掩码的稀疏度。"""
        if mask.shape[0] == 1:
            print("current_sparsity:", 1-mask.sum().item() / mask.numel())
            return ((1 - mask.sum().item() / mask.numel()) * mask.shape[1] + 0.9 * (96 - mask.shape[1])) / 96
        return 1 - mask.sum().item() / mask.numel()

    def _record_sparsity(self, sample_idx, timestep, layeridx, sparsity):
        """记录稀疏度信息。"""
        self.sparsity_records[sample_idx]["records"].append({
            "timestep": timestep,
            "layer": layeridx,
            "sparsity": sparsity
        })
        print(Fore.MAGENTA + f"Sample {sample_idx}, Timestep {timestep}, Layer {layeridx}: Sparsity = {sparsity:.4f}" + Style.RESET_ALL)

    def _save_sparsity_records(self, sample_idx):
        """保存稀疏度记录到 JSON 文件。"""
        filename = f"sparsity_record_sample_{sample_idx}.json"
        with open(filename, "w") as f:
            json.dump(self.sparsity_records[sample_idx], f, indent=4)

    @preserve_rng_state
    @timeit
    def sparse_gen_forward(self, q, k, v):
        """稀疏前向传播，生成或更新掩码并计算注意力输出。"""
        self.sm_scale = 1 / q.size(-1) ** 0.5
        counter = self.counter % (self.layernum * self.timestep)
        current_layer = counter % self.layernum
        current_timestep = counter // self.layernum
        current_k = self.k_list[current_timestep] if current_timestep < 4 else 0.1
        max_retain_ratio = self.max_retain_ratio_list[current_timestep]
        min_retain_ratio = self.min_retain_ratio_list[current_timestep]
        energy_threshold = self.energy_threshold_list[current_timestep]

        pool = calc_attn_block_sum_efficient(q, k, num_keep=self.block_size // 8, block_size=self.block_size)
        self.mask[current_layer] = transfer_attn_to_mask(pool, mode="energy", init_k=current_k,
                                                        max_retain_ratio=max_retain_ratio,
                                                        min_retain_ratio=min_retain_ratio,
                                                        energy_threshold=energy_threshold)
        out = self.block_sparse_triton_fn(q, k, v, self.mask[current_layer], self.sm_scale)

        sparsity = self._calculate_sparsity(self.mask[current_layer])
        sample_idx = self.counter // (self.layernum * self.timestep)
        self._record_sparsity(sample_idx, current_timestep, current_layer, sparsity)
        return out

    def need_update(self, counter):
        """判断是否需要更新掩码。"""
        return (counter // self.layernum) in self.update_list

    def __call__(self, q, k, v, use_rearranger=True):
        """执行前向传播，支持 warmup 阶段和稀疏计算。"""
        counter = self.counter % (self.layernum * self.timestep)
        if counter // self.layernum < self.warmup_epoch:
            out = torch.nn.functional.scaled_dot_product_attention(q, k, v)
        else:
            out_std= torch.nn.functional.scaled_dot_product_attention(q, k, v)
            if(use_rearranger):
                q, k, v = self.rearranger.rearrange(q, k, v)
                out = self.sparse_gen_forward(q, k, v)
                out = self.rearranger.reversed_rearrange(out)
            else:
                out = self.sparse_gen_forward(q, k, v)
            diff= out - out_std
            print("mean diff:", torch.mean(diff.abs()))

        self.counter += 1
        if self.need_update(self.counter):
            self.mask = [None] * self.layernum
        if self.counter % (self.layernum * self.timestep) == 0:
            sample_idx = (self.counter // (self.layernum * self.timestep)) - 1
            self._save_sparsity_records(sample_idx)
            print(f"save_sparsity_records to sparsity_record_sample_{sample_idx}.json")
        return out