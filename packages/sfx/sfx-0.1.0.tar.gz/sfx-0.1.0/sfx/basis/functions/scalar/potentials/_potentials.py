"""Potentials"""

__all__ = [
    "lennard_jones",
    "lennard_jones_2n_n",
    "lennard_jones_attraction",
    "lennard_jones_repulsion",
    "truncated_lennard_jones",
    "wca",
    "shoulder",
]

import jax
import jax.numpy as jnp
from jax import lax
from jax.tree_util import Partial


@Partial
def lennard_jones(r, parameters):
    return (
        4
        * parameters.epsilon
        * (jnp.divide(parameters.sigma, r) ** 12 - jnp.divide(parameters.sigma, r) ** 6)
    )


@Partial
def lennard_jones_2n_n(r, parameters):
    return (
        4
        * parameters.epsilon
        * (
            jnp.power(jnp.divide(parameters.sigma, r), 2 * parameters.n)
            - jnp.power(jnp.divide(parameters.sigma, r), parameters.n)
        )
    )


@Partial
def lennard_jones_repulsion(r, parameters):
    return 4 * parameters.epsilon * jnp.divide(parameters.sigma, r) ** 12


@Partial
def lennard_jones_attraction(r, parameters):
    return -4 * parameters.epsilon * jnp.divide(parameters.sigma, r) ** 6


@Partial
def truncated_lennard_jones(r, parameters):
    return lax.cond(
        r < 2.5 * parameters.sigma,
        lambda r, parameters: lennard_jones(r, parameters)
        - lennard_jones(2.5 * parameters.sigma, parameters),
        lambda *_: 0.0,
        r,
        parameters,
    )


@Partial
def wca(r, parameters):
    return lax.cond(
        r < 2 ** (1.0 / 6) * parameters.sigma,
        lambda r, parameters: lennard_jones(r, parameters) + parameters.epsilon,
        lambda *_: 0.0,
        r,
        parameters,
    )


@Partial
def shoulder(r, parameters):
    sigma_h = parameters.sigma_h
    sigma_s = parameters.sigma_s

    epsilon_h = parameters.epsilon
    epsilon_s = parameters.epsilon_s

    n = parameters.n
    k0 = parameters.k0

    hard_repulsion = epsilon_h * jnp.power(sigma_h / r, n)
    soft_repulsion = 0.5 * epsilon_s * (1 - jnp.tanh(k0 * (r - sigma_s)))

    return hard_repulsion + soft_repulsion
