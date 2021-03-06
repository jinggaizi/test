# Copyright 2019 Shigeki Karita
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

"""Mask module."""

import torch


def subsequent_mask(size, device="cpu", dtype=torch.bool):
    """Create mask for subsequent steps (size, size).

    :param int size: size of mask
    :param str device: "cpu" or "cuda" or torch.Tensor.device
    :param torch.dtype dtype: result dtype
    :rtype: torch.Tensor
    >>> subsequent_mask(3)
    [[1, 0, 0],
     [1, 1, 0],
     [1, 1, 1]]
    """
    ret = torch.ones(size, size, device=device, dtype=dtype)
    return torch.tril(ret, out=ret)

def subsequent_mask_limit(size, left_context, device="cpu", dtype=torch.bool):
    """Create mask for subsequent steps (1, size, size).
    :param int size: size of mask
    :param str device: "cpu" or "cuda" or torch.Tensor.device
    :param torch.dtype dtype: result dtype
    :rtype: torch.Tensor
    >>> subsequent_mask(3)
    [[1, 0, 0],
     [1, 1, 0],
     [1, 1, 1]
    """
    ret = torch.ones(size, size, device=device, dtype=dtype)
    return torch.triu(torch.tril(ret), diagonal=-left_context, out=ret)

def target_mask(ys_in_pad, ignore_id):
    """Create mask for decoder self-attention.

    :param torch.Tensor ys_pad: batch of padded target sequences (B, Lmax)
    :param int ignore_id: index of padding
    :param torch.dtype dtype: result dtype
    :rtype: torch.Tensor (B, Lmax, Lmax)
    """
    ys_mask = ys_in_pad != ignore_id
    m = subsequent_mask(ys_mask.size(-1), device=ys_mask.device).unsqueeze(0)
    return ys_mask.unsqueeze(-2) & m

def target_mask_limit(ys_in_pad, ignore_id, left_context):
    """Create mask for decoder self-attention.

    :param torch.Tensor ys_pad: batch of padded target sequences (B, Lmax)
    :param int ignore_id: index of padding
    :param torch.dtype dtype: result dtype
    :rtype: torch.Tensor
    """
    ys_mask = ys_in_pad != ignore_id
    m = subsequent_mask_limit(ys_mask.size(-1), left_context, device=ys_mask.device).unsqueeze(0)
    return ys_mask.unsqueeze(-2) & m
