# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from typing import Optional

import torch
from torch import nn, Tensor

from sam2.modeling.sam.transformer import RoPEAttention

from sam2.modeling.sam2_utils import get_activation_fn, get_clones
import pdb

class MemoryAttentionLayer(nn.Module):

    def __init__(
        self,
        activation: str,
        cross_attention: nn.Module,
        d_model: int,
        dim_feedforward: int,
        dropout: float,
        pos_enc_at_attn: bool,
        pos_enc_at_cross_attn_keys: bool,
        pos_enc_at_cross_attn_queries: bool,
        self_attention: nn.Module,
    ):
        super().__init__()
        self.d_model = d_model
        self.dim_feedforward = dim_feedforward
        self.dropout_value = dropout
        self.self_attn = self_attention
        self.cross_attn_image = cross_attention

        # Implementation of Feedforward model
        self.linear1 = nn.Linear(d_model, dim_feedforward)
        self.dropout = nn.Dropout(dropout)
        self.linear2 = nn.Linear(dim_feedforward, d_model)

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        self.dropout3 = nn.Dropout(dropout)

        self.activation_str = activation
        self.activation = get_activation_fn(activation)

        # Where to add pos enc
        self.pos_enc_at_attn = pos_enc_at_attn
        self.pos_enc_at_cross_attn_queries = pos_enc_at_cross_attn_queries
        self.pos_enc_at_cross_attn_keys = pos_enc_at_cross_attn_keys

    def _forward_sa(self, tgt, query_pos):
        # Self-Attention
        tgt2 = self.norm1(tgt)
        q = k = tgt2 + query_pos if self.pos_enc_at_attn else tgt2
        tgt2 = self.self_attn(q, k, v=tgt2)
        tgt = tgt + self.dropout1(tgt2)
        return tgt

    def _forward_ca(self, tgt, memory, query_pos, pos, num_k_exclude_rope=0, object_frame_scores=None, object_ptr_scores=None):
        kwds = {}
        if num_k_exclude_rope > 0:
            assert isinstance(self.cross_attn_image, RoPEAttention)
            kwds = {"num_k_exclude_rope": num_k_exclude_rope}
        
        # Cross-Attention
        tgt2 = self.norm2(tgt)
        if object_frame_scores is None: 
            key = memory + pos if self.pos_enc_at_cross_attn_keys else memory
        else: # relative
            key_original = memory + pos if self.pos_enc_at_cross_attn_keys else memory
            num_frame, num_ptr = len(object_frame_scores), len(object_ptr_scores)
            num_frame_ = int(num_frame*4096)
            num_object = key_original.shape[0]
            key_frame = key_original[:, :num_frame_].reshape(num_object, num_frame, 4096, -1)
            key_ptr = key_original[:, num_frame_:].reshape(num_object, num_ptr, 4, -1)
            scaling_low = 0.95
            scaling_high = 1.05
            if num_frame == 1:
                key = key_original
            else:
                weight_frame = torch.stack(object_frame_scores, dim=1) # num_object, num_frame
                weight_ptr = torch.stack(object_ptr_scores, dim=1) # num_object, num_ptr

                standard_weight_frame = torch.linspace(scaling_low, scaling_high, num_frame).to(weight_frame) # num_frame
                standard_weight_ptr = torch.linspace(scaling_low, scaling_high, num_ptr).to(weight_ptr) # num_ptr

                new_weight_frame = torch.zeros_like(weight_frame)
                new_weight_ptr = torch.zeros_like(weight_ptr)

                new_weight_frame.scatter_(1, torch.argsort(weight_frame, dim=1), standard_weight_frame.unsqueeze(0).repeat([num_object, 1]))
                new_weight_ptr.scatter_(1, torch.argsort(weight_ptr, dim=1), standard_weight_ptr.unsqueeze(0).repeat([num_object, 1]))
                
                key_frame_scale = (new_weight_frame[:, :, None, None].to(key_frame.device) * key_frame)
                key_ptr_scale = (new_weight_ptr[:, :, None, None].to(key_ptr.device) * key_ptr)
                key = torch.cat([key_frame_scale.reshape(num_object, num_frame_, -1), key_ptr_scale.reshape(num_object, int(num_ptr*4), -1)], dim=1)
        # key = memory + pos if self.pos_enc_at_cross_attn_keys else memory
        tgt2 = self.cross_attn_image(
            q=tgt2 + query_pos if self.pos_enc_at_cross_attn_queries else tgt2,
            k=key,
            v=memory,
            **kwds,
        )
        tgt = tgt + self.dropout2(tgt2)
        return tgt

    def forward(
        self,
        tgt,
        memory,
        pos: Optional[Tensor] = None,
        query_pos: Optional[Tensor] = None,
        num_k_exclude_rope: int = 0,
        object_frame_scores = None,
        object_ptr_scores = None,
    ) -> torch.Tensor:

        # Self-Attn, Cross-Attn
        tgt = self._forward_sa(tgt, query_pos)
        tgt = self._forward_ca(tgt, memory, query_pos, pos, num_k_exclude_rope, object_frame_scores, object_ptr_scores)
        # MLP
        tgt2 = self.norm3(tgt)
        tgt2 = self.linear2(self.dropout(self.activation(self.linear1(tgt2))))
        tgt = tgt + self.dropout3(tgt2)
        return tgt


class MemoryAttention(nn.Module):
    def __init__(
        self,
        d_model: int,
        pos_enc_at_input: bool,
        layer: nn.Module,
        num_layers: int,
        batch_first: bool = True,  # Do layers expect batch first input?
    ):
        super().__init__()
        self.d_model = d_model
        self.layers = get_clones(layer, num_layers)
        self.num_layers = num_layers
        self.norm = nn.LayerNorm(d_model)
        self.pos_enc_at_input = pos_enc_at_input
        self.batch_first = batch_first

    def forward(
        self,
        curr: torch.Tensor,  # self-attention inputs
        memory: torch.Tensor,  # cross-attention inputs
        curr_pos: Optional[Tensor] = None,  # pos_enc for self-attention inputs
        memory_pos: Optional[Tensor] = None,  # pos_enc for cross-attention inputs
        num_obj_ptr_tokens: int = 0,  # number of object pointer *tokens*
        object_frame_scores=None,
        object_ptr_scores=None,
    ):
        if isinstance(curr, list):
            assert isinstance(curr_pos, list)
            assert len(curr) == len(curr_pos) == 1
            curr, curr_pos = (
                curr[0],
                curr_pos[0],
            )

        assert (
            curr.shape[1] == memory.shape[1]
        ), "Batch size must be the same for curr and memory"

        output = curr
        if self.pos_enc_at_input and curr_pos is not None:
            output = output + 0.1 * curr_pos

        if self.batch_first:
            # Convert to batch first
            output = output.transpose(0, 1)
            curr_pos = curr_pos.transpose(0, 1)
            memory = memory.transpose(0, 1)
            memory_pos = memory_pos.transpose(0, 1)

        for layer in self.layers:
            kwds = {}
            if isinstance(layer.cross_attn_image, RoPEAttention):
                kwds = {"num_k_exclude_rope": num_obj_ptr_tokens,
                        "object_frame_scores": object_frame_scores,
                        "object_ptr_scores":object_ptr_scores}

            output = layer(
                tgt=output,
                memory=memory,
                pos=memory_pos,
                query_pos=curr_pos,
                **kwds,
            )
        normed_output = self.norm(output)

        if self.batch_first:
            # Convert back to seq first
            normed_output = normed_output.transpose(0, 1)
            curr_pos = curr_pos.transpose(0, 1)

        return normed_output