import torch
from block_sparse_attn import block_sparse_attn_func
from einops import rearrange
from block_sparse_attn.bert_padding import pad_input, unpad_input
from special_attentions.utils.attn_pooling_kernel import attn_with_pooling
from special_attentions.utils.gilbert3d import gilbert3d
############parameters###############
# 这里的参数是根据实际情况设置的，可能需要根据具体任务进行调整
width=85
height=48
depth=11
sample_num=128
text_length=224
sparsity_bound=0.8
#####################################
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

    return mask

def judge_sparsity(q,k):
    def get_softmax(q, k):
        scale_factor = 1.0 / (q.size(-1) ** 0.5)
        out=torch.matmul(q, k.transpose(-2, -1)) * scale_factor
        out=out-out.max(dim=-1, keepdim=True)[0]
        out = torch.softmax(out, dim=-1)
        return out
    #通过前百分之二十的元素占的attn权重来判断稀疏性，大于0.8为稀疏
    idx_for_q = torch.randperm(width * height)[:sample_num] + text_length
    q=q[:,:,idx_for_q]
    k=k[:,:,::3]
    attn=get_softmax(q,k)
    attn=attn.sort(dim=-1,descending=True)[0].mean(dim=-2)
    sparsity=attn[:,:,:int(k.size(-2)*0.2)].sum(dim=-1)>sparsity_bound
    return sparsity

def generate_qkv(q, k, v, query_padding_mask=None, key_padding_mask=None):
    """
    Convert q, k, v tensors for block-sparse attention.
    Args:
        q: (batch_size, seqlen_q, nheads, d)
        k: (batch_size, seqlen_k, nheads_k, d)
        v: (batch_size, seqlen_k, nheads_k, d)
        query_padding_mask: (batch_size, seqlen_q), bool, optional
        key_padding_mask: (batch_size, seqlen_k), bool, optional
    Returns:
        q_unpad, k_unpad, v_unpad, cu_seqlens_q, cu_seqlens_k, max_seqlen_q, max_seqlen_k, q, k, v, output_pad_fn, dq_pad_fn, dk_pad_fn
    """
    batch_size, seqlen_q, nheads, d = q.shape
    _, seqlen_k, nheads_k, _ = k.shape
    assert k.shape == (batch_size, seqlen_k, nheads_k, d)
    assert v.shape == (batch_size, seqlen_k, nheads_k, d)

    if query_padding_mask is not None:
        q_unpad, indices_q, cu_seqlens_q, max_seqlen_q = unpad_input(q, query_padding_mask)
        output_pad_fn = lambda output_unpad: pad_input(output_unpad, indices_q, batch_size, seqlen_q)
    else:
        q_unpad = rearrange(q, "b s h d -> (b s) h d")
        cu_seqlens_q = torch.arange(0, (batch_size + 1) * seqlen_q, step=seqlen_q, dtype=torch.int32, device=q.device)
        max_seqlen_q = seqlen_q
        output_pad_fn = lambda output_unpad: rearrange(output_unpad, "(b s) h d -> b s h d", b=batch_size)

    if key_padding_mask is not None:
        k_unpad, indices_k, cu_seqlens_k, max_seqlen_k = unpad_input(k, key_padding_mask)
        v_unpad, _, _, _ = unpad_input(v, key_padding_mask)
    else:
        k_unpad = rearrange(k, "b s h d -> (b s) h d")
        v_unpad = rearrange(v, "b s h d -> (b s) h d")
        cu_seqlens_k = torch.arange(0, (batch_size + 1) * seqlen_k, step=seqlen_k, dtype=torch.int32, device=k.device)
        max_seqlen_k = seqlen_k

    dq_pad_fn = output_pad_fn
    dk_pad_fn = lambda dk_unpad: rearrange(dk_unpad, "(b s) h d -> b s h d", b=batch_size) if key_padding_mask is None else pad_input(dk_unpad, indices_k, batch_size, seqlen_k)
    
    return (
        q_unpad, k_unpad, v_unpad, cu_seqlens_q, cu_seqlens_k, max_seqlen_q, max_seqlen_k, 
        q, k, v, output_pad_fn, dq_pad_fn, dk_pad_fn
    )

def block_sparse_attn(q, k, v, block_mask):
    """
    Block-sparse attention mechanism.
    Args:
        q: (batch_size, nheads, seqlen, d)
        k: (batch_size, nheads, seqlen, d)
        v: (batch_size, nheads, seqlen, d)
        block_mask: (batch_size, nheads, blocks_q, blocks_k), bool
    Returns:
        out: (batch_size, nheads, seqlen, d)
    """
    batch_size, nheads, seqlen, d = q.shape
    device = q.device
    query_padding_mask = torch.ones(batch_size, seqlen, dtype=torch.bool, device=device)
    key_padding_mask = torch.ones(batch_size, seqlen, dtype=torch.bool, device=device)
    q_unpad, k_unpad, v_unpad, cu_seqlens_q, cu_seqlens_k, max_seqlen_q, max_seqlen_k, _, _, _, output_pad_fn, _, _ = generate_qkv(
        q.transpose(1, 2), k.transpose(1, 2), v.transpose(1, 2), query_padding_mask, key_padding_mask
    )
    base_blockmask = block_mask.contiguous()
    head_mask_type = torch.ones(nheads, dtype=torch.int32, device=device)
    streaming_info = torch.zeros(2 * nheads, dtype=torch.int32, device=device)
    out_unpad = block_sparse_attn_func(
        q_unpad, k_unpad, v_unpad, cu_seqlens_q, cu_seqlens_k, head_mask_type, streaming_info, base_blockmask,
        max_seqlen_q, max_seqlen_k, p_dropout=0.0, deterministic=True, softmax_scale=None, is_causal=False,
        exact_streaming=False, return_attn_probs=False
    )
    out = output_pad_fn(out_unpad)
    out = out.view(batch_size, seqlen, nheads, d)
    out = out.permute(0, 2, 1, 3)
    return out




def adaptive_block_sparse_attn(q, k, v):
    """
    Adaptive block-sparse attention mechanism.
    Creates a block mask automatically (based on q, k) without gradient tracking for mask steps.
    Args:
        q: (batch_size, nheads, seqlen, d)
        k: (batch_size, nheads, seqlen, d)
        v: (batch_size, nheads, seqlen, d)
    Returns:
        out: (batch_size, nheads, seqlen, d)
    """
    causal = False
    sm_scale = 1.0 / (q.size(-1) ** 0.5)
    block_size = 128
    # Disable gradient tracking for pooling and mask operations
    with torch.no_grad():
        _, pooling = attn_with_pooling(q, k, v, causal, sm_scale, block_size)
        mask = transfer_attn_to_mask(
            pooling,
            mode="energy",
            init_k=None,
            max_retain_ratio=0.7,
            min_retain_ratio=0.05,
            energy_threshold=0.95
        )
    # Perform block-sparse attention with the computed mask (gradients flow here)
    out = block_sparse_attn(q, k, v, mask)
    return out

import torch.nn as nn

class AdaptiveBlockSparseAttnTrain(nn.Module):
    def __init__(self):
        super().__init__()
        self.gilbert_rearranger = GilbertRearranger(width, height, depth, text_length)

    def forward(self, q, k, v):
        # Rearrange inputs via Gilbert curve ordering
        q_r, k_r, v_r = self.gilbert_rearranger.rearrange(q, k, v)
        # Compute block-sparse attention without tracking gradients for pooling and mask creation
        out_r = adaptive_block_sparse_attn(q_r, k_r, v_r)
        # Reverse the arrangement
        out = self.gilbert_rearranger.reversed_rearrange(out_r)
        return out