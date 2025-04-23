"""Forces"""

__all__ = [
    "active_force",
    "constant_force",
    "constant",
    "inverse",
    "linear_force",
    "square_wave",
]

from jax.tree_util import Partial
from jax import lax
import jax.numpy as jnp
from sfx.basis.parameters import Parameters


@Partial
def active_force(coordinate, parameters: Parameters):
    """Computes an active force in the direction of coordinate.orientation."""
    return parameters.activity * coordinate.orientation


@Partial
def constant_force(_, parameters):
    return parameters.coefficient * parameters.axis


@Partial
def linear_force(coordinate, param):
    return (
        param.coefficient
        * jnp.dot(param.axis, (coordinate.position - param.origin))
        + param.constant
    ) * param.axis


@Partial
def square_wave(r_ij, parameters):
    r = jnp.linalg.norm(r_ij)

    return lax.cond(
        (r > parameters.min) & (r < parameters.max),
        lambda: jnp.true_divide(r_ij, r),
        lambda: jnp.zeros_like(r_ij),
    )


@Partial
def constant(r_ij, parameters):
    r = jnp.linalg.norm(r_ij)
    return parameters.constant * jnp.true_divide(r_ij, r)


@Partial
def inverse(r_ij, parameters):
    r = jnp.linalg.norm(r_ij)
    return parameters.constant * jnp.true_divide(r_ij, r) * jnp.reciprocal(r)
