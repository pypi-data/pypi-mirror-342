""""""
__all__ = [
    "reduce_coordinates",
    "select_coordinates",
    "surface_coordinates",
    "constant_direction",
]

from functools import wraps

import jax
import jax.numpy as jnp
from jax.tree_util import Partial


def reduce_coordinates(func, indices=slice(None), **jitkw):
    @wraps(func)
    @Partial
    def wrapper(q_i, *args, **kwargs):
        return (
            jnp.zeros_like(q_i).at[indices].set(func(q_i.at[indices], *args, **kwargs))
        )

    return wrapper


def select_coordinates(func, selector=Partial(lambda q_i: q_i), **jitkw):
    @wraps(func)
    @Partial
    def wrapper(q_i, *args, **kwargs):
        return func(selector(q_i), *args, **kwargs)

    return wrapper


def surface_coordinates(func, axis, origin, **jitkw):
    @wraps(func)
    @Partial
    def wrapper(coordinates, *args, **kwargs):
        distance = jnp.dot(axis, coordinates.position - origin)
        return func(distance, *args, **kwargs) * axis

    return wrapper


def constant_direction(func, direction, **jitkw):
    @wraps(func)
    @Partial
    def wrapper(coordinates, *args, **kwargs):
        distance = jnp.dot(direction, coordinates.position)
        return func(distance, *args, **kwargs) * direction

    return wrapper
