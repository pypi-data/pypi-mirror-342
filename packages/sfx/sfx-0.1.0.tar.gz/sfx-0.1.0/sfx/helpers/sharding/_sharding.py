"""JAX sharding utilities"""

__all__ = ["shard_sum_function", "shard_function", "create_mesh"]

import os
from typing import Callable
from functools import partial, wraps
from jax.sharding import Mesh, PartitionSpec
from jax.experimental.shard_map import shard_map
from jax.experimental import mesh_utils

import jax
import jax.numpy as jnp


def create_mesh(names, shape: tuple[int] = (len(jax.devices()),)):
    devices = mesh_utils.create_device_mesh(shape)
    mesh = Mesh(devices, axis_names=names)
    return mesh


def shard_sum_function(func: Callable, mesh: Mesh, axis_name: str) -> Callable:
    """Maps a function over shards of data with communication (sum).
    function args are mapped while kwargs are shared.
    The mapped function should always return a tuple.
    """

    def scan_func(carry, args):
        kwargs = carry[0]
        old_carry = carry[1]

        new_kwargs, new_values = func(*args, **kwargs)
        new_carry = (
            new_kwargs,
            jax.tree_util.tree_map(lambda oc, nv: oc + nv, old_carry, new_values),
            # tuple(oc + nv for oc, nv in zip(old_carry, new_values)),
        )
        return (new_carry, None)

    @wraps(func)
    def sharded(*args, **kwargs):
        seq_length = (len(args[0]) - 1) % len(mesh.devices)

        # init_args = tuple(arg[0] for arg in args)
        init_args = jax.tree_util.tree_map(lambda arg: arg[0], args)
        init = func(*init_args, **kwargs)

        if seq_length:
            # seq_data = tuple(arg[1 : seq_length + 1] for arg in args)
            # sharded_data = tuple(arg[1 + seq_length :] for arg in args)
            seq_data = jax.tree_util.tree_map(lambda arg: arg[1 : seq_length + 1], args)
            sharded_data = jax.tree_util.tree_map(
                lambda arg: arg[1 + seq_length :], args
            )
            init = jax.lax.scan(scan_func, init, seq_data)[0]
        else:
            # sharded_data = tuple(arg[1:] for arg in args)
            sharded_data = jax.tree_util.tree_map(lambda arg: arg[1:], args)

        # _init = (init[0], tuple(jnp.zeros_like(i) for i in init[1]))
        _init = (init[0], jax.tree_util.tree_map(lambda i: jnp.zeros_like(i), init[1]))
        in_specs = tuple([PartitionSpec(axis_name) for _ in args])
        # out_specs = (PartitionSpec(None), tuple(PartitionSpec(None) for _ in init[1]))
        out_specs = (
            PartitionSpec(None),
            jax.tree_util.tree_map(lambda _: PartitionSpec(None), init[1]),
        )

        @partial(
            shard_map,
            mesh=mesh,
            in_specs=in_specs,
            out_specs=out_specs,
            check_rep=False,
        )
        def _sharded(*args):
            kwargs, arrays = jax.lax.scan(scan_func, _init, args)[0]
            return (kwargs, jax.lax.psum(arrays, axis_name=axis_name))

        lkwargs, arrays = _sharded(*sharded_data)
        return (
            lkwargs,
            # tuple(i + f for i, f in zip(init[1], arrays))
            jax.tree_util.tree_map(lambda i, f: i + f, init[1], arrays),
        )

    return sharded


def shard_function(func: Callable, mesh: Mesh, axis_name: str) -> Callable:
    """Maps a function over shards of data without communication.
    function args are mapped while kwargs are shared.
    The mapped function should always return a tuple.
    """

    def scan_func(carry, args):
        kwargs = carry
        return (carry, func(*args, **kwargs))

    @wraps(func)
    def sharded(*args, **kwargs):
        seq_length = (len(args[0]) - 1) % len(mesh.devices)

        # init_args = tuple(arg[0] for arg in args)
        init_args = jax.tree_util.tree_map(lambda arg: arg[0], args)
        _init_arrays = func(*init_args, **kwargs)
        _init_kwargs = kwargs

        # print(seq_length)#, len(args[0]), _init_kwargs)
        if seq_length:
            # seq_data = tuple(arg[1 : seq_length + 1] for arg in args)
            # sharded_data = tuple(arg[1 + seq_length :] for arg in args)
            # init_arrays = tuple(
            #     jnp.append(i[jnp.newaxis, ...], _a, axis=0)
            #     for i, _a in zip(_init_arrays, _arrays)
            # )

            seq_data = jax.tree_util.tree_map(lambda arg: arg[1 : seq_length + 1], args)
            sharded_data = jax.tree_util.tree_map(
                lambda arg: arg[1 + seq_length :], args
            )
            init_kwargs, _arrays = jax.lax.scan(scan_func, _init_kwargs, seq_data)

            init_arrays = jax.tree_util.tree_map(
                lambda i, _a: jnp.append(i[jnp.newaxis, ...], _a, axis=0),
                _init_arrays,
                _arrays,
            )
        else:
            # sharded_data = tuple(arg[1:] for arg in args)
            # init_arrays = tuple(_init[jnp.newaxis, ...] for _init in _init_arrays)

            sharded_data = jax.tree_util.tree_map(lambda arg: arg[1:], args)
            init_kwargs = _init_kwargs
            init_arrays = jax.tree_util.tree_map(
                lambda _init: _init[jnp.newaxis, ...], _init_arrays
            )

        in_specs = tuple([PartitionSpec(axis_name)] * len(args))
        # out_specs = tuple([PartitionSpec(axis_name)] * len(init_arrays))
        out_specs = jax.tree_util.tree_map(
            lambda _: PartitionSpec(axis_name), init_arrays
        )

        # print(
        #     in_specs, out_specs, jax.tree_util.tree_map(lambda i: i.shape, init_arrays)
        # )

        @partial(
            shard_map,
            mesh=mesh,
            in_specs=in_specs,
            out_specs=out_specs,
            check_rep=False,
        )
        def _sharded(*args):
            return jax.lax.scan(scan_func, init_kwargs, args)[-1]

        arrays = _sharded(*sharded_data)
        # return tuple(jnp.append(i, f, axis=0) for i, f in zip(init_arrays, arrays))
        return jax.tree_util.tree_map(
            lambda i, f: jnp.append(i, f, axis=0), init_arrays, arrays
        )

    return sharded
