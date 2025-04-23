"""Helpers to homogenize data format."""

__all__ = [
    "expand_dimensions",
    "match_dof",
    "fix_arguments",
    "set_parameters",
    "vmap_function",
    "make_func_differentiable",
    "homogenize",
]

from functools import wraps, update_wrapper
from sfx.helpers.math import find_pattern_index
from jax.tree_util import Partial

import jax
import jax.numpy as jnp


def match_dof(func, coordinates, names: list | str):
    """Fill the output with zeros such that the output shape
    matches the dof.

    :param func: The function on which output should be filled.
    :param length: The length of the output.
    :param indices: The indices in the output where the function
    output will be set.

    :return: An output-filled function.
    """

    if isinstance(names, list):
        name = names[0]
        sl = coordinates.offset[name]
        indices = jnp.arange(sl.start, sl.stop, sl.step)

        for name in names[1:]:
            sl = coordinates.offset[name]
            indices = jnp.append(indices, jnp.arange(sl.start, sl.stop, sl.step))

        indices = jnp.sort(indices)

    elif isinstance(names, str):
        sl = coordinates.offset[names]
        indices = jnp.arange(sl.start, sl.stop, sl.step)

    @wraps(func)
    @Partial
    def wrapper(*args, **kwargs):
        values = func(*args, **kwargs)
        output = jnp.zeros((coordinates.dof,))

        # This select
        output = output.at[indices].set(values)

        return output

    return wrapper


def fix_arguments(func, use_time: bool = False):
    """Fix the function arguments to match the default
    argument specification (coordinates, time, parameters).

    :param func: The function to fix.
    :param use_time: Whether the function being fixed depends on time.

    :return: An argument-specification fixed function.
    """

    @wraps(func)
    @Partial
    def wrapper(*args, time, parameters):
        if use_time:
            output = func(*args, time, parameters)
        else:
            output = func(*args, parameters)

        return output

    return wrapper


def vmap_function(func, vmapkw={}):
    """Vmap the function arguments.

    :param func: The function to vmap.
    :param jitkw: Dictionnary with jit options.
    :param vmapkw: Dictionnary with vmap options.

    :return: A jitted and vmapped function.
    """

    @wraps(func)
    @Partial
    def wrapper(*args, **kwargs):
        return jax.vmap(func, **vmapkw)(*args, **kwargs)

    return wrapper


def set_parameters(func, **parameters):
    """Set the function parameters to fix values.

    :param func: The function to set parameters.
    :param parameters: The parameters to use.

    :return: A parameter-fixed function.
    """

    return update_wrapper(Partial(func, **parameters), func)


# @partial(jax.jit, static_argnames=("axes",))
@Partial
def expand_dimensions(source, target, axes=(0,)):
    """Expands the dimensions of source to match target's dimensions around fix axes."""
    shape = target.shape
    newshape = (
        [1 for _ in shape[: axes[0]]]
        + [shape[axis] for axis in axes]
        + [1 for _ in shape[axes[-1] + 1 :]]
    )
    return source.reshape(newshape)


def _extract_differentiable_parameters(parameters, argnums=(0,), allow_int=False):
    """Extract parameters to retain only differentiable ones."""

    def tell_include(leaf):
        leaf_dtype = jax.core.get_aval(leaf).dtype
        return jax.dtypes.issubdtype(
            leaf_dtype, jnp.inexact
        ) | allow_int * jax.dtypes.issubdtype(leaf_dtype, jnp.integer)

    include = jnp.empty(0)
    include_idx = []
    exclude = []
    exclude_idx = []
    tree_defs = []

    for p, param in enumerate(parameters):
        iidx = []
        eidx = []

        flattened, tree_def = jax.tree_util.tree_flatten(param)
        if p in argnums:
            for i, val in enumerate(flattened):
                if tell_include(val):
                    iidx.append(i)
                    include = jnp.append(include, val)
                else:
                    eidx.append(i)
                    exclude.append(val)
        else:
            for i, val in enumerate(flattened):
                eidx.append(i)
                # exclude.append(val)

        include_idx.append(iidx)
        exclude_idx.append(eidx)
        tree_defs.append(tree_def)

    return tree_defs, (include, include_idx), (exclude, exclude_idx)


def _insert_differentiable_parameters(trees, included, excluded):
    """Insert differentiable parameters back into their initial structure.
    Reverts the operation of 'extract_differentiable_parameters'.
    """

    args = []

    include, include_idx = included
    exclude, exclude_idx = excluded

    offset_include = 0
    offset_exclude = 0

    for tree, iidx, eidx in zip(trees, include_idx, exclude_idx):
        # print(tree, iidx, eidx)
        all_leaves = []

        for i, idx in enumerate(iidx):
            all_leaves.insert(idx, include[i + offset_include])

        for i, idx in enumerate(eidx):
            all_leaves.insert(idx, exclude[i + offset_exclude])

        args.append(jax.tree_util.tree_unflatten(tree, all_leaves))

        offset_include += len(iidx)
        offset_exclude += len(eidx)

    args = tuple(args)

    return args


def make_func_differentiable(
    func,
    *args,
    argnums=(0,),
):
    """
    Create a function for which differentiation can always be performed.
    """
    trees, included, excluded = _extract_differentiable_parameters(
        args, argnums=argnums
    )

    differentiable_args = included[0]

    @wraps(func)
    @Partial
    def wrapper(differentiable_args, *args, **kwargs):
        flattened_args, _ = jax.tree_util.tree_flatten(list(args))
        new_args = _insert_differentiable_parameters(
            trees,
            (differentiable_args, included[-1]),
            (excluded[0] + flattened_args, excluded[-1]),
        )
        return func(*new_args, **kwargs)

    def recombine(differentiable_args):
        return _insert_differentiable_parameters(
            [trees[0]],
            (differentiable_args, [included[-1][0]]),
            (excluded[0], [excluded[-1][0]]),
        )[0]

    return wrapper, differentiable_args, recombine


@Partial
def homogenize(source, target):
    "Homogenize source to target shape"
    src_shape = jnp.asarray(source.shape)
    trgt_shape = jnp.asarray(target.shape)

    index = find_pattern_index(trgt_shape, src_shape)[0]

    axis = [
        i
        for i in range(len(trgt_shape))
        if (i < index) or (i > index + len(src_shape) - 1)
    ]
    return jnp.broadcast_to(jnp.expand_dims(source, axis=axis), target.shape)
