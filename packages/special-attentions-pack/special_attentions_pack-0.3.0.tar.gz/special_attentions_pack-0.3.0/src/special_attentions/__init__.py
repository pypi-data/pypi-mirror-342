"""
special_attentions: 一组稀疏注意力机制实现
"""

# from .Golden_attention import Golden_attention
# from .LocalGlobalAttention import LocalGlobalAttention
from .MergeAttention import MergeAttention
# from .SildingTileAttention import SildingTileAttention
from .SmartAttention import SmartAttention
from .SparseGen_Plus import BlockSparseAttention
from .combined_attn import CombinedAttn
from .partern_attention import ParternAttentionColVersion_V3,ParternAttentionColVersion_V4

__all__ = [
    "MergeAttention",
    "SmartAttention",
    "BlockSparseAttention",
    "CombinedAttn",
    "ParternAttentionColVersion_V3",
    "ParternAttentionColVersion_V4",
]
