import torch
from special_attentions.partern_attention import ParternAttentionColVersion_V3,ParternAttentionColVersion_V4, unified_judge
from special_attentions.SparseGen_Plus import BlockSparseAttention
from special_attentions.utils.tools import preserve_rng_state
from colorama import Fore, Style

class CombinedAttn:
    """A class combining pattern-based and block-sparse attention mechanisms.

    This class integrates `ParternAttentionColVersion_V3` and `BlockSparseAttention` to process
    queries, keys, and values dynamically based on a warmup period and pattern judgment.
    """

    @preserve_rng_state
    def __init__(self, warmup_epoch=8, block_size=128, layer_num=42, timestep=50):
        """Initialize the CombinedAttn class with attention mechanisms and counters.

        Args:
            warmup_epoch (int): Number of initial epochs to use block-sparse attention only.
            block_size (int): Size of blocks for block-sparse attention.
            layer_num (int): Number of layers in the model.
            timestep (int): Total timesteps per cycle.
        """
        self.block_size = block_size
        self.layer_num = layer_num
        self.timestep = timestep
        self.warmup_epoch = warmup_epoch
        
        # Initialize attention mechanisms
        self.pattern_attn = ParternAttentionColVersion_V4()
        self.block_sparse_attn = BlockSparseAttention(
            block_size=block_size,
            layernum=layer_num,
            timestep=timestep,
            num_samples=50,
            warmup_epoch=warmup_epoch
        )
        
        # Counters for tracking steps and pattern usage
        self.step_counter = 0
        self.pattern_usage_counter = 0

    def __call__(self, q, k, v, use_rearranger=False):
        """Forward pass combining pattern and block-sparse attention.

        Args:
            q (torch.Tensor): Query tensor of shape [batch, heads, seq_len, dim].
            k (torch.Tensor): Key tensor of shape [batch, heads, seq_len, dim].
            v (torch.Tensor): Value tensor of shape [batch, heads, seq_len, dim].
            use_rearranger (bool): Whether to use rearranger and recover functions.

        Returns:
            torch.Tensor: Output tensor of the same shape as q.
        """
        # Calculate current timestep within the cycle
        current_time = (self.step_counter // self.layer_num) % self.timestep
        self.step_counter += 1

        # During warmup, use only block-sparse attention
        if current_time < self.warmup_epoch:
            output = self.block_sparse_attn(q, k, v)
            print(output.abs().mean())
            return output

        # Decide which positions use pattern attention
        use_pattern = unified_judge(q, k)
        output = torch.zeros_like(q)
        print("use_pattern:", use_pattern.float().mean())
        if use_pattern.any():
            # Track pattern usage
            pattern_count = use_pattern.float().sum()
            self.pattern_usage_counter += pattern_count

            # Extract pattern-selected inputs
            q_pat = q[use_pattern].unsqueeze(0)
            k_pat = k[use_pattern].unsqueeze(0)
            v_pat = v[use_pattern].unsqueeze(0)

            # Process pattern attention
            if pattern_count > 48:
                # Split into two parts if sequence length exceeds 48
                q1, k1, v1 = q_pat[:, :48], k_pat[:,  :48], v_pat[:,  :48]
                attn_1 = self.pattern_attn(q1, k1, v1)
                q2, k2, v2 = q_pat[:,  48:], k_pat[:,  48:], v_pat[:,  48:]
                attn_2 = self.pattern_attn(q2, k2, v2)
                attn_pat = torch.cat([attn_1, attn_2], dim=1)
            else:
                attn_pat = self.pattern_attn(q_pat, k_pat, v_pat)

            # Assign pattern attention output
            output[use_pattern] = attn_pat.squeeze()

            # Process remaining positions with block-sparse attention if any
            if (~use_pattern).any():
                q_sparse = q[~use_pattern].unsqueeze(0)
                k_sparse = k[~use_pattern].unsqueeze(0)
                v_sparse = v[~use_pattern].unsqueeze(0)

                # Compute block-sparse attention
                attn_sparse = self.block_sparse_attn(q_sparse, k_sparse, v_sparse,use_rearranger=use_rearranger)


                # Assign sparse attention output
                output[~use_pattern] = attn_sparse.squeeze(0)
        else:
            # Use block-sparse attention for all positions
            output = self.block_sparse_attn(q, k, v)

        # Log pattern usage
        print(
            Fore.GREEN + f"counter: {self.pattern_usage_counter}, "
            f"now increment: {use_pattern.float().sum()}" + Style.RESET_ALL
        )
        return output

    # Placeholder for rearranger and recover methods (to be implemented if needed)
    def rearranger(self, q, k, v):
        """Rearrange inputs for block-sparse attention."""
        raise NotImplementedError("Rearranger method not implemented.")

    def recover(self, attn):
        """Recover original layout after block-sparse attention."""
        raise NotImplementedError("Recover method not implemented.")