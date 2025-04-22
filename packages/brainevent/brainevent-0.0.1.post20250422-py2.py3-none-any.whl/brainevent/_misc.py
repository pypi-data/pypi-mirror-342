# Copyright 2025 BDP Ecosystem Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# -*- coding: utf-8 -*-

from typing import Tuple, NamedTuple

import brainunit as u
import jax
import jax.numpy as jnp
from jax.experimental.sparse import csr_todense_p, coo_todense_p

from ._typing import MatrixShape, Data, Index


class COOInfo(NamedTuple):
    """
    A named tuple containing metadata for COO (Coordinate) format sparse matrices.

    COO format represents a sparse matrix using three arrays: data values, row indices,
    and column indices. This class stores shape and sorting information needed for
    sparse matrix operations.

    Attributes:
        shape: Sequence[int]
            The shape of the matrix as a sequence of integers (rows, columns).
        rows_sorted: bool, default=False
            Indicates whether the row indices are in sorted order.
        cols_sorted: bool, default=False
            Indicates whether the column indices are in sorted order within each row.
            Only relevant if ``rows_sorted`` is True.
    """
    shape: MatrixShape
    rows_sorted: bool = False
    cols_sorted: bool = False


def _coo_todense(
    data: Data,
    row: Index,
    col: Index,
    *,
    spinfo: COOInfo
) -> Data:
    """Convert CSR-format sparse matrix to a dense matrix.

    Args:
      data : array of shape ``(nse,)``.
      row : array of shape ``(nse,)``
      col : array of shape ``(nse,)`` and dtype ``row.dtype``
      spinfo : COOInfo object containing matrix metadata

    Returns:
      mat : array with specified shape and dtype matching ``data``
    """
    data, unit = u.split_mantissa_unit(data)
    r = coo_todense_p.bind(data, row, col, spinfo=spinfo)
    return u.maybe_decimal(r * unit)


@jax.jit
def _csr_to_coo(indices: jax.Array, indptr: jax.Array) -> Tuple[jax.Array, jax.Array]:
    """Given CSR (indices, indptr) return COO (row, col)"""
    return jnp.cumsum(jnp.zeros_like(indices).at[indptr].add(1)) - 1, indices


def _csr_todense(
    data: Data,
    indices: Index,
    indptr: Index,
    *,
    shape: MatrixShape
) -> Data:
    """
    Convert CSR-format sparse matrix to a dense matrix.

    Args:
      data : array of shape ``(nse,)``.
      indices : array of shape ``(nse,)``
      indptr : array of shape ``(shape[0] + 1,)`` and dtype ``indices.dtype``
      shape : length-2 tuple representing the matrix shape

    Returns:
      mat : array with specified shape and dtype matching ``data``
    """
    data, unit = u.split_mantissa_unit(data)
    mat = csr_todense_p.bind(data, indices, indptr, shape=shape)
    return u.maybe_decimal(mat * unit)


def general_batching_rule(prim, args, axes, **kwargs):
    """
    Implements a general batching rule for JAX primitive operations.

    This function handles batching for JAX primitives by separating batched and non-batched
    arguments, then applying the primitive to each element in the batch using jax.lax.scan.

    Args:
        prim: The JAX primitive operation to be batched.
        args: Sequence of input arguments to the primitive.
        axes: Sequence of axis indices indicating the batch dimension for each argument.
              None indicates that the corresponding argument is not batched.
        **kwargs: Additional keyword arguments to pass to the primitive.

    Returns:
        tuple: A tuple containing:
            - outs: The batched outputs from applying the primitive.
            - out_dim: A pytree with the same structure as outs, indicating
              the batch dimensions of each output.

    Note:
        This function moves all batch dimensions to the leading axis (0) before
        applying scan, then processes each slice of the batched inputs.
    """
    batch_axes, batch_args, non_batch_args = [], {}, {}
    for ax_i, ax in enumerate(axes):
        if ax is None:
            non_batch_args[f'ax{ax_i}'] = args[ax_i]
        else:
            batch_args[f'ax{ax_i}'] = args[ax_i] if ax == 0 else jax.numpy.moveaxis(args[ax_i], ax, 0)
            batch_axes.append(ax_i)

    def f(_, x):
        """
        Internal function for jax.lax.scan that applies the primitive to a single batch element.

        Args:
            _: Carry value (unused).
            x: Dictionary containing the current batch slice for each batched argument.

        Returns:
            tuple: (carry value, primitive output)
        """
        pars = tuple(
            [(x[f'ax{i}'] if i in batch_axes else non_batch_args[f'ax{i}'])
             for i in range(len(axes))]
        )
        return 0, prim.bind(*pars, **kwargs)

    _, outs = jax.lax.scan(f, 0, batch_args)
    out_vals, out_tree = jax.tree.flatten(outs)
    out_dim = jax.tree.unflatten(out_tree, (0,) * len(out_vals))
    return outs, out_dim
