"""Helpers for simulation runs and results."""

__all__ = ["sliding_window"]

import jax
import jax.numpy as jnp
from jax.tree_util import Partial, tree_flatten, tree_unflatten


def sliding_window(obj, step, width=2, funcs=None):
    leaves, tree = tree_flatten(obj)

    if funcs is None:
        funcs = [Partial(lambda x: jnp.diff(x, axis=0))] * len(leaves)

    def _stepper(i, leaves):
        shape = leaves[i].shape
        return jax.lax.fori_loop(
            0,
            width,
            lambda k, value: value.at[k].set(leaves[i + k * step]),
            jnp.zeros((width, *shape), dtype=leaves.dtype),
        )

    def _slide(i, values):
        return [
            val.at[i].set(funcs[j](_stepper(i, leaves[j])))
            for j, val in enumerate(values)
        ]

    new_length = len(obj) - (width - 1) * step
    new_leaves = jax.lax.fori_loop(
        0,
        new_length,
        body_fun=_slide,
        init_val=leaves,
    )

    new_obj = tree_unflatten(
        tree,
        [nl[:new_length] for nl in new_leaves],
    )
    return new_obj
