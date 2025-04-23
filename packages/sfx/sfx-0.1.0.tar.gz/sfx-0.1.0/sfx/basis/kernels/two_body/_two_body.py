""""""

__all__ = [
    "distance_vector",
    "distance_vector_pbc",
    "distance_vector_pbc_param",
    "distance_vector_pbc_lattice",
    "pairwise_spherical",
    "generalized_distance",
    "generalized_pairwise",
]

from functools import wraps

import jax
import jax.numpy as jnp
from jax.tree_util import Partial

from sfx.helpers.math import compute_nearest_image_lattice

# jaxtyping shape definitions
# _dim    = "dim"
# _scalar = ""


# def radial(
#     x_i: jt.Float[jt.Array, _dim], x_j: jt.Float[jt.Array, _dim]
# ) -> Tuple[jt.Float[jt.Array, _scalar], jt.Float[jt.Array, _dim]]:
#     """Computes the radial distance and normalised radial vector.
#
#     The radial distance is :math:`r = \\left| r_{ij} \\right|_{2}` and
#     the normalised radial vector :math:`\\hat{r}_{ij} = r_{ij}/r` with
#     :math:`r_{ij} = x_i - x_j`.
#
#     :param x_i: First coordinate :math:`x_i`.
#     :param x_j: Second coordinate :math:`x_j`.
#
#     :return: The radial distance :math:`r` and normalised radial vector :math:`\\hat{r}_{ij}`.
#
#     """
#
#     r_ij: jt.Float[jt.Array, _dim] = jnp.subtract(x_i, x_j)
#     r: jt.Float[jt.Array, _scalar] = jnp.linalg.norm(r_ij)
#     e_ij: jt.Float[jt.Array, _dim] = jnp.true_divide(r_ij, r)
#
#     return (r, e_ij)


def distance_vector(func, **jitkw):
    # @partial(jax.jit, **jitkw)
    @wraps(func)
    @Partial
    def wrapper(coord_i, coord_j, *args, **kwargs):
        # Compute the distance and restrict
        distance = jnp.subtract(coord_i.position, coord_j.position)
        return func(distance, *args, **kwargs)

    return wrapper


def generalized_distance(func, distance_func=jnp.subtract, name="position"):
    """Computes a distance_func for a pair of coordinates named name."""

    # @partial(jax.jit, **jitkw)
    @wraps(func)
    @Partial
    def wrapper(coord_i, coord_j, *args, **kwargs):
        # Compute the distance
        distance = distance_func(coord_i[name], coord_j[name])
        return func(distance, *args, **kwargs)

    return wrapper


# @jax.jit
@Partial
def _compute_minimum_image(distance, pbc):
    # convert nan to zero as nan in pbc means no periodic boundary
    return distance - jnp.nan_to_num(jnp.rint((distance - pbc.min) / pbc.max) * pbc.max)


def distance_vector_pbc(func, pbc, **jitkw):
    """Transform the input of a function to the minimum image convention (MIC)
    distance with periodic boundary conditions (PBC)

    :param func: The function that will take the MIC distance as input
    :param pbc: The Periodic Boundary Condtions
    :param jitkw: Keyword arguments to pass to `jax.jit`

    :return: A composed function where any pair of input coordinates will
    be converted to a mic distance.
    """

    # @partial(jax.jit, **jitkw)
    @wraps(func)
    @Partial
    def wrapper(coord_i, coord_j, *args, **kwargs):
        # Compute the distance vector
        distance = jnp.subtract(coord_i.position, coord_j.position)

        # Apply the Minimum Image Convention (MIC) only on `position`` components.
        # Useful in the case of having different types of coordinates, e.g,
        # use (MIC) only on position and not orientation.

        mic_distance = _compute_minimum_image(distance, pbc)
        return jnp.nan_to_num(func(mic_distance, *args, **kwargs))

    return wrapper


def distance_vector_pbc_param(func):
    """Transform the input of a function to the minimum image convention (MIC)
    distance with periodic boundary conditions (PBC)

    :param func: The function that will take the MIC distance as input
    :param jitkw: Keyword arguments to pass to `jax.jit`

    :return: A composed function where any pair of input coordinates will
    be converted to a mic distance using the pbc in parameters.
    """

    # @partial(jax.jit, **jitkw)
    @wraps(func)
    @Partial
    def wrapper(coord_i, coord_j, parameters, *args, **kwargs):
        # Compute the distance vector
        distance = jnp.subtract(coord_i.position, coord_j.position)

        # Apply the Minimum Image Convention (MIC) only on `position`` components.
        # Useful in the case of having different types of coordinates, e.g,
        # use (MIC) only on position and not orientation.

        mic_distance = _compute_minimum_image(distance, parameters.pbc)
        return jnp.nan_to_num(func(mic_distance, *(*args, parameters), **kwargs))

    return wrapper


def distance_vector_pbc_lattice(func):
    """Transform the input of a function to the minimum image convention (MIC)
    distance with periodic boundary conditions (PBC)

    :param func: The function that will take the MIC distance as input
    :param jitkw: Keyword arguments to pass to `jax.jit`

    :return: A composed function where any pair of input coordinates will
    be converted to a mic distance using the pbc in parameters.
    """

    @wraps(func)
    @Partial
    def wrapper(coord_i, coord_j, parameters, *args, **kwargs):
        distance = jnp.subtract(coord_i.position, coord_j.position)
        mic_distance = compute_nearest_image_lattice(distance, parameters.pbc)
        return jnp.nan_to_num(func(mic_distance, *(*args, parameters), **kwargs))

    return wrapper


def pairwise_spherical(func, jitkw={}):
    # @partial(jax.jit, **jitkw)
    @wraps(func)
    @Partial
    def wrapper(r_ij, *args, **kwargs):
        r = jnp.linalg.norm(r_ij)

        return jax.lax.cond(
            r,
            lambda: jnp.true_divide(r_ij, r) * func(r, *args, **kwargs),
            lambda: jnp.zeros_like(r_ij),
        )

    return wrapper


def generalized_pairwise(func, modifier=jnp.linalg.norm, jitkw={}):
    # @partial(jax.jit, **jitkw)
    @wraps(func)
    @Partial
    def wrapper(q_ij, *args, **kwargs):
        q = modifier(q_ij)

        return jax.lax.cond(
            q,
            lambda: jnp.true_divide(q_ij, q) * func(q, *args, **kwargs),
            lambda: jnp.zeros_like(q_ij),
        )

    return wrapper
