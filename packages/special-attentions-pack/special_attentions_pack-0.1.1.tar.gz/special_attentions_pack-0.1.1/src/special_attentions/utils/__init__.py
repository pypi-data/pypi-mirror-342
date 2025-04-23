"""
工具函数：注意力相关的底层实现
"""
from .attn_pooling_kernel import attn_with_pooling
from .gilbert3d import gilbert3d 
from .block_sparse_attn_kernel import sparse_attention_factory,block_sparse_triton_fn
# … 按需导入

__all__ = [
    "AttnMeanKernel",
    "attn_with_pooling",
    "gilbert3d",
    "sparse_attention_factory",
    "block_sparse_triton_fn",
]
