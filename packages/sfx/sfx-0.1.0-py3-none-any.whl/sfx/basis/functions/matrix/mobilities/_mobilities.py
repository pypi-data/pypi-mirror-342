"""Mobilities"""

__all__ = ["rpy", "rpy_periodic", "uncoupled"]


import jax
import jax.numpy as jnp
import jax.scipy as jsp
from jax import lax
from jax.tree_util import Partial

from sfx.helpers.math import (
    compute_nearest_image_lattice,
    create_levi_civita_symbol,
    particle_mesh_ewald,
)


@Partial
def translation_translational(r_ij, parameters):
    radius = parameters.radius
    viscosity = parameters.viscosity

    self_mobility = jnp.reciprocal(6 * jnp.pi * viscosity * radius)

    r = jnp.linalg.norm(r_ij)

    # if i == j, then we get a nan instead of 0 because of the
    # division by the length of the distance vector.
    e_ij = jnp.nan_to_num(jnp.divide(r_ij, r))

    _identity = jnp.eye(r_ij.shape[0])
    _ee = jnp.outer(e_ij, e_ij)

    return lax.cond(
        r > 2.0 * radius,
        lambda: jnp.reciprocal(8.0 * jnp.pi * r * viscosity)
        * (
            (1.0 + jnp.divide(2.0 * radius**2, 3.0 * r**2)) * _identity
            + (1.0 - jnp.divide(2.0 * radius**2, r**2)) * _ee
        ),
        lambda: self_mobility
        * (
            (1.0 - jnp.divide(9.0 * r, 32.0 * radius)) * _identity
            + jnp.divide(3.0 * r, 32.0 * radius) * _ee
        ),
    )


@Partial
def rotational_rotational(r_ij, parameters):
    radius = parameters.radius
    viscosity = parameters.viscosity

    self_mobility = jnp.reciprocal(8.0 * jnp.pi * viscosity * radius**3)

    r = jnp.linalg.norm(r_ij)

    # if i == j, then we get a nan instead of 0 because of the
    # division by the length of the distance vector.
    e_ij = jnp.nan_to_num(jnp.divide(r_ij, r))

    _identity = jnp.eye(r_ij.shape[0])
    _ee = jnp.outer(e_ij, e_ij)

    return lax.cond(
        r > 2.0 * radius,
        lambda: -jnp.reciprocal(16.0 * jnp.pi * viscosity * r**3)
        * (_identity - 3.0 * _ee),
        lambda: self_mobility
        * (
            (
                1.0
                - jnp.divide(27.0 * r, 32.0 * radius)
                + jnp.divide(5.0 * r**3, 64.0 * radius**3)
            )
            * _identity
            + (
                jnp.divide(9.0 * r, 32.0 * radius)
                - jnp.divide(3.0 * r**3, 64.0 * radius**3)
            )
            * _ee
        ),
    )


@Partial
def rotational_translational(r_ij, parameters):
    radius = parameters.radius
    viscosity = parameters.viscosity

    r = jnp.linalg.norm(r_ij)
    e_ij = jnp.nan_to_num(jnp.true_divide(r_ij, r))
    _epsilonr = jnp.dot(
        create_levi_civita_symbol(r_ij.shape[0]),
        e_ij,
    )

    return lax.cond(
        r > 2.0 * radius,
        lambda: jnp.reciprocal(8.0 * jnp.pi * viscosity * r**2) * _epsilonr,
        lambda: jnp.reciprocal(16.0 * jnp.pi * viscosity * radius**2)
        * (jnp.divide(r, radius) - jnp.divide(3.0 * r**2, 8.0 * radius**2))
        * _epsilonr,
    )


@Partial
def rpy(r_ij, parameters, mode=Partial(lambda: "translation")):
    if mode() == "translation":
        tensor = translation_translational(r_ij, parameters)

    else:
        coupling_tt = translation_translational(r_ij, parameters)
        coupling_rr = rotational_rotational(r_ij, parameters)
        coupling_rt = rotational_translational(r_ij, parameters)

        tensor = jnp.block([[coupling_tt, coupling_rt.T], [coupling_rt, coupling_rr]])

    return tensor


@Partial
def uncoupled(r_ij, parameters):
    """Computes the mobility for uncoupled system.

    parameters:
        - self_mobility :
    """
    return lax.cond(
        jnp.linalg.norm(r_ij) == 0.0,
        lambda: parameters.self_mobility,
        lambda: jnp.zeros_like(parameters.self_mobility),
    )


# # Self interaction #
# def Mtt_self(radius, parameters):
#     dim = parameters.direct_lattice.shape[-1]
#     cell_volume = jnp.linalg.det(parameters.direct_lattice)
#     _identity = jnp.eye(dim)
#     _split2 = parameters.splitting**2
#     _a2 = radius**2
#     _frac = jnp.reciprocal(
#         4 * jnp.sqrt(2 * jnp.pi**3) * parameters.splitting * parameters.viscosity,
#     )
#
#     _term_1 = (
#         _frac
#         * (jnp.true_divide(_a2, 9 * _split2) - 1)
#         # - 0.5 * jnp.true_divide(_split2, parameters.viscosity * cell_volume)
#     ) * _identity
#
#     _sum = Mtt(jnp.zeros(dim), radius, parameters)
#
#     # def _direct_term(r, r_ij):
#     #     _r2 = r**2
#     #
#     #     term_1 = Mtt_np(r_ij, radius, radius) * jsp.special.erfc(
#     #         jnp.true_divide(r, jnp.sqrt(2) * parameters.splitting)
#     #     )
#     #
#     #     term_2 = (
#     #         _frac
#     #         * jnp.exp(-0.5 * jnp.true_divide(_r2, _split2))
#     #         * (
#     #             (jnp.true_divide(_a2, 3 * _split2) + jnp.true_divide(2 * _a2, 3 * _r2))
#     #             * _identity
#     #             + (
#     #                 1
#     #                 + jnp.true_divide(_a2 * _r2, 3 * _split2**2)
#     #                 - jnp.true_divide(2 * _a2, 3 * _split2)
#     #                 - jnp.true_divide(2 * _a2, _r2)
#     #             )
#     #             * jnp.outer(r_ij, r_ij)
#     #         )
#     #     )
#     #
#     #     return term_1 + term_2
#     #
#     # def _reciprocal_term(k2, k_ij):
#     #     term_3 = (
#     #         jnp.reciprocal(parameters.viscosity * cell_volume)
#     #         * (_identity - (1 + 0.5 * _split2 * k2) * jnp.outer(k_ij, k_ij))
#     #         * (1 - jnp.true_divide(_a2, 3) * k2)
#     #         * jnp.reciprocal(k2)
#     #         * jnp.exp(-0.5 * k2 * _split2)
#     #     )
#     #     return term_3
#
#     # def _sum_term(cell_vector, direct_lattice, reciprocal_lattice):
#     #     r_ij = jnp.dot(direct_lattice, cell_vector)
#     #     r = jnp.linalg.norm(r_ij)
#     #     k_ij = jnp.dot(cell_vector, reciprocal_lattice)
#     #     k2 = jnp.dot(k_ij, k_ij)
#     #
#     #     return jax.lax.cond(
#     #         jnp.any(cell_vector),
#     #         _reciprocal_term,
#     #         lambda _: jnp.zeros_like(_identity),
#     #         r,
#     #         k2,
#     #         jnp.true_divide(r_ij, r),
#     #         jnp.true_divide(k_ij, jnp.sqrt(k2)),
#     #     )
#
#     # _sum = jnp.sum(
#     #     jax.vmap(_sum_term, in_axes=(0, None, None))(
#     #         parameters.cell_vector,
#     #         parameters.direct_lattice,
#     #         parameters.reciprocal_lattice,
#     #     ),
#     #     axis=0,
#     # )
#     # _sum = particle_mesh_ewald(
#     #     lambda r, r_ij: jax.lax.cond(
#     #         r,
#     #         _direct_term(r, r_ij),
#     #         lambda *_: jnp.zeros_like(_identity),
#     #     ),
#     #     _reciprocal_term,
#     # )(jnp.zeros(dim), parameters)
#
#     return _term_1 + _sum
#
#
# def Mrr_self(parameters):
#     dim = parameters.direct_lattice.shape[-1]
#     # cell_volume = jnp.linalg.det(parameters.direct_lattice)
#     _identity = jnp.eye(dim)
#     # _split2 = parameters.splitting**2
#
#     # def _direct_term(r, r_ij):
#     #     _r2 = r**2
#     #
#     #     term_1 = Mrr_np(r_ij) * jsp.special.erfc(
#     #         jnp.true_divide(r, jnp.sqrt(2) * parameters.splitting)
#     #     )
#     #
#     #     term_2 = (
#     #         3
#     #         * jnp.exp(-0.5 * jnp.true_divide(_r2, _split2))
#     #         * jnp.reciprocal(
#     #             16
#     #             * jnp.sqrt(2 * jnp.pi**3)
#     #             * parameters.viscosity
#     #             * parameters.splitting,
#     #         )
#     #         * (
#     #             (jnp.reciprocal(3 * _split2) + jnp.true_divide(2, 3 * _r2)) * _identity
#     #             + (
#     #                 jnp.true_divide(_r2, 3 * _split2**2)
#     #                 - jnp.true_divide(2, 3 * _split2)
#     #                 - jnp.true_divide(2, _r2)
#     #             )
#     #             * jnp.outer(r_ij, r_ij)
#     #         )
#     #     )
#     #     return term_1 - term_2
#     #
#     # def _reciprocal_term(k2, k_ij):
#     #
#     #     term_3 = (
#     #         jnp.reciprocal(4 * parameters.viscosity * cell_volume)
#     #         * (_identity - (1 + 0.5 * _split2 * k2) * jnp.outer(k_ij, k_ij))
#     #         * jnp.exp(-0.5 * k2 * _split2)
#     #     )
#     #
#     #     return term_3
#
#     _term_1 = (
#         -jnp.reciprocal(
#             48
#             * jnp.sqrt(2 * jnp.pi**3)
#             * parameters.splitting**3
#             * parameters.viscosity
#         )
#         * _identity
#     )
#
#     _sum = Mrr(jnp.zeros(dim), parameters)
#     # particle_mesh_ewald(
#     #     lambda r, r_ij: jax.lax.cond(
#     #         r,
#     #         _direct_term(r, r_ij),
#     #         lambda *_: jnp.zeros_like(_identity),
#     #     ),
#     #     _reciprocal_term,
#     # )(jnp.zeros(dim), parameters)
#
#     return _term_1 + _sum
#
#
# def Mrt_self():
#     return 0.0


# Periodic RPY #
# Non-Periodic terms #
@Partial
def Mtt_np(r, r_ij, A_ij2, parameters):
    return jnp.reciprocal(8.0 * jnp.pi * parameters.viscosity * r) * (
        (1.0 + jnp.divide(2.0 * A_ij2, 3.0 * r**2)) * jnp.eye(r_ij.shape[0])
        + (1.0 - jnp.divide(2.0 * A_ij2, r**2)) * jnp.outer(r_ij, r_ij)
    )


@Partial
def Mrr_np(r, r_ij, parameters):
    return jnp.reciprocal(16.0 * jnp.pi * parameters.viscosity * r**3) * (
        3 * jnp.outer(r_ij, r_ij) - jnp.eye(r_ij.shape[0])
    )


@Partial
def Mrt_np(r, r_ij, parameters):
    _epsilon = create_levi_civita_symbol(r_ij.shape[0])
    return jnp.reciprocal(8.0 * jnp.pi * parameters.viscosity * r**2) * (
        jnp.dot(_epsilon, r_ij)
    )


# Regularization terms #
@Partial
def Ytt(r_ij, a_i, a_j, parameters):
    _dim = parameters.pbc.direct_lattice.shape[-1]
    _add = a_i + a_j
    _sub = a_i - a_j

    r = jnp.linalg.norm(r_ij)
    _r2 = r**2
    _r3 = r**3

    e_ij = jnp.true_divide(r_ij, r)

    _identity = jnp.eye(_dim)

    a_large, a_small = jnp.asarray([a_i, a_j]) * (_sub >= 0) + jnp.asarray(
        [a_j, a_i]
    ) * (_sub < 0)

    def _Ytt_1():
        return jnp.reciprocal(6.0 * jnp.pi * parameters.viscosity * a_i * a_j) * (
            (0.5 * _add - jnp.true_divide((_sub**2 + 3 * _r2) ** 2, 32 * _r3))
            * _identity
            + jnp.true_divide(3 * (_sub**2 - _r2) ** 2, 32 * _r3)
            * jnp.outer(e_ij, e_ij)
        )

    def _Ytt_2():
        return jnp.reciprocal(6.0 * jnp.pi * parameters.viscosity * a_large) * _identity

    return jax.lax.cond(
        r > a_large - a_small,
        _Ytt_1,
        _Ytt_2,
    ) - Mtt_np(r, e_ij, jnp.true_divide(a_i**2 + a_j**2, 2.0), parameters)
    # return jax.lax.cond(
    #     r <= _add,
    #     lambda: jax.lax.cond(
    #         r > a_large - a_small,
    #         _Ytt_1,
    #         _Ytt_2,
    #     )
    #     - Mtt_np(r, r_ij, jnp.true_divide(a_i**2 + a_j**2, 2.0), parameters),
    #     lambda: jnp.zeros((_dim, _dim)),
    # )


@Partial
def Yrr(r_ij, a_i, a_j, parameters):
    dim = parameters.pbc.direct_lattice.shape[-1]
    _sub = a_i - a_j

    r = jnp.linalg.norm(r_ij)
    _r2 = r**2
    _r3 = r**3
    e_ij = jnp.true_divide(r_ij, r)

    _a_i2 = a_i**2
    _a_j2 = a_j**2

    a_large, a_small = jnp.asarray([a_i, a_j]) * (_sub >= 0) + jnp.asarray(
        [a_j, a_i]
    ) * (_sub < 0)

    _identity = jnp.eye(dim)

    def _Yrr_1():
        return jnp.reciprocal(8.0 * jnp.pi * parameters.viscosity * a_i**3 * a_j**3) * (
            jnp.true_divide(
                5 * r**6
                - 27 * r**4 * (_a_i2 + _a_j2)
                + 32 * _r3 * (a_i**3 + a_j**3)
                - 9 * _r2 * (_a_i2 - _a_j2) ** 2
                - (_a_i2 + 4 * a_i * a_j + _a_j2) * (a_i - a_j) ** 4,
                64 * _r3,
            )
            * _identity
            + jnp.true_divide(
                3 * (_a_i2 + 4 * a_i * a_j + _a_j2 - _r2) * (_sub**2 - _r2) ** 2,
                64 * _r3,
            )
            * jnp.outer(e_ij, e_ij)
        )

    def _Yrr_2():
        return (
            jnp.reciprocal(8.0 * jnp.pi * parameters.viscosity * a_large**3) * _identity
        )

    return jax.lax.cond(
        r > a_large - a_small,
        _Yrr_1,
        _Yrr_2,
    ) - Mrr_np(r, e_ij, parameters)

    # return jax.lax.cond(
    #     r <= a_i + a_j,
    #     lambda: jax.lax.cond(
    #         r > a_large - a_small,
    #         _Yrr_1,
    #         _Yrr_2,
    #     )
    #     - Mrr_np(r, r_ij, parameters),
    #     lambda: jnp.zeros((dim, dim)),
    # )


@Partial
def Yrt(r_ij, a_i, a_j, parameters):
    dim = parameters.pbc.direct_lattice.shape[-1]
    _sub = a_i - a_j
    r = jnp.linalg.norm(r_ij)
    e_ij = jnp.true_divide(r_ij, r)
    a_large, a_small = jnp.asarray([a_i, a_j]) * (_sub >= 0) + jnp.asarray(
        [a_j, a_i]
    ) * (_sub < 0)

    _epsilonr = jnp.dot(
        create_levi_civita_symbol(r_ij.shape[0]),
        e_ij,
    )

    def _Yrt_1():
        return jnp.reciprocal(16.0 * jnp.pi * parameters.viscosity * a_i**3 * a_j) * (
            jnp.true_divide(
                (a_j**2 + 2 * a_j * (a_i + r) - 3 * (a_i - r) ** 2) * (_sub + r) ** 2,
                8 * r**2,
            )
            * _epsilonr
        )

    def _Yrt_2():
        return jax.lax.cond(
            a_j < a_i,
            lambda: jnp.divide(r, 8.0 * jnp.pi * parameters.viscosity * a_i**3)
            * _epsilonr,
            lambda: jnp.zeros((dim, dim)),
        )

    return jax.lax.cond(
        r > a_large - a_small,
        _Yrt_1,
        _Yrt_2,
    ) - Mrt_np(r, e_ij, parameters)
    # return jax.lax.cond(
    #     r <= a_i + a_j,
    #     lambda: jax.lax.cond(
    #         r > a_large - a_small,
    #         _Yrt_1,
    #         _Yrt_2,
    #     )
    #     ,
    #     lambda: jnp.zeros((dim, dim)),
    # )


# mobility interaction #
def Mtt(r_ij, A_ij2, parameters):
    _dim = parameters.pbc.direct_lattice.shape[-1]
    _cell_volume = parameters.pbc.direct_volume
    _identity = jnp.eye(_dim)
    _split2 = parameters.splitting**2

    def _direct_term(r_n, r_ij_n, parameters):
        _r_n2 = r_n**2
        _term_1 = Mtt_np(r_n, r_ij_n, A_ij2, parameters) * jsp.special.erfc(
            jnp.true_divide(r_n, jnp.sqrt(2) * parameters.splitting)
        )

        _term_2 = (
            jnp.reciprocal(
                4.0
                * jnp.sqrt(2 * jnp.pi**3)
                * parameters.viscosity
                * parameters.splitting
            )
            * jnp.exp(-0.5 * jnp.true_divide(_r_n2, _split2))
        ) * (
            (
                jnp.true_divide(A_ij2, 3 * _split2)
                + jnp.true_divide(2 * A_ij2, 3 * _r_n2)
            )
            * _identity
            + (
                1
                + jnp.true_divide(A_ij2 * _r_n2, 3 * _split2**2)
                - jnp.true_divide(2 * A_ij2, 3 * _split2)
                - jnp.true_divide(2 * A_ij2, _r_n2)
            )
            * jnp.outer(r_ij_n, r_ij_n)
        )

        return _term_1 + _term_2

    def _reciprocal_term(k_n2, k_ij_n, parameters):
        _term_1 = (
            (
                jnp.reciprocal(parameters.viscosity * _cell_volume * k_n2)
                * jnp.exp(-0.5 * k_n2 * _split2)
                * jnp.cos(jnp.sqrt(k_n2) * jnp.dot(k_ij_n, r_ij))
            )
            * (1 - jnp.reciprocal(3) * A_ij2 * k_n2)
            * (_identity - (1 + 0.5 * _split2 * k_n2) * jnp.outer(k_ij_n, k_ij_n))
        )
        return _term_1

    # _sum = particle_mesh_ewald(_direct_sum_term, _reciprocal_sum_term)(r_ij, parameters)
    _sum = particle_mesh_ewald(
        lambda r, r_ij, parameters: jax.lax.cond(
            r,
            lambda: _direct_term(r, r_ij, parameters),
            lambda: jnp.zeros_like(_identity),
        ),
        _reciprocal_term,
    )(r_ij, parameters)

    return (
        _sum
        - 0.5
        * jnp.true_divide(_split2, parameters.viscosity * _cell_volume)
        * _identity
    )


def Mrr(r_ij, parameters):
    _dim = parameters.pbc.direct_lattice.shape[-1]
    _cell_volume = parameters.pbc.direct_volume
    _identity = jnp.eye(_dim)
    _split2 = parameters.splitting**2

    def _direct_term(r_n, r_ij_n, parameters):
        _r_n2 = r_n**2
        _term_1 = Mrr_np(r_n, r_ij_n, parameters) * jsp.special.erfc(
            jnp.true_divide(r_n, jnp.sqrt(2) * parameters.splitting)
        )

        _term_2 = (
            3
            * (
                jnp.reciprocal(
                    16.0
                    * jnp.sqrt(2 * jnp.pi**3)
                    * parameters.viscosity
                    * parameters.splitting
                )
                * jnp.exp(-0.5 * jnp.true_divide(_r_n2, _split2))
            )
            * (
                (jnp.reciprocal(3 * _split2) + 2 * jnp.reciprocal(3 * _r_n2))
                * _identity
                + (
                    jnp.true_divide(_r_n2, 3 * _split2**2)
                    - 2 * jnp.reciprocal(3 * _split2)
                    - 2 * jnp.reciprocal(_r_n2)
                )
                * jnp.outer(r_ij_n, r_ij_n)
            )
        )

        return _term_1 - _term_2

    def _reciprocal_term(k_n2, k_ij_n, parameters):
        _term_1 = (
            jnp.reciprocal(4 * parameters.viscosity * _cell_volume)
            * jnp.exp(-0.5 * k_n2 * _split2)
            * jnp.cos(jnp.sqrt(k_n2) * jnp.dot(k_ij_n, r_ij))
        ) * (_identity - (1 + 0.5 * _split2 * k_n2) * jnp.outer(k_ij_n, k_ij_n))
        return _term_1

    # _sum = particle_mesh_ewald(_direct_sum_term, _reciprocal_sum_term)(r_ij, parameters)

    _sum = particle_mesh_ewald(
        lambda r, r_ij, parameters: jax.lax.cond(
            r,
            lambda: _direct_term(r, r_ij, parameters),
            lambda: jnp.zeros_like(_identity),
        ),
        _reciprocal_term,
    )(r_ij, parameters)

    return _sum


def Mrt(r_ij, parameters):
    _dim = parameters.pbc.direct_lattice.shape[-1]
    _cell_volume = parameters.pbc.direct_volume
    _epsilon = create_levi_civita_symbol(_dim)
    _split2 = parameters.splitting**2

    def _direct_sum_term(r_n, r_ij_n, parameters):
        _r_n2 = r_n**2
        _term_1 = Mrt_np(r_n, r_ij_n, parameters) * jsp.special.erfc(
            jnp.true_divide(r_n, jnp.sqrt(2) * parameters.splitting)
        )

        _term_2 = (
            jnp.reciprocal(
                r_n
                * 4.0
                * jnp.sqrt(2 * jnp.pi**3)
                * parameters.viscosity
                * parameters.splitting
            )
            * jnp.exp(-0.5 * jnp.true_divide(_r_n2, _split2))
            * jnp.dot(_epsilon, r_ij_n)
        )

        return _term_1 + _term_2

    def _reciprocal_sum_term(k_n2, k_ij_n, parameters):
        _term_1 = (
            jnp.reciprocal(2 * parameters.viscosity * _cell_volume * jnp.sqrt(k_n2))
            * jnp.exp(-0.5 * k_n2 * _split2)
            * jnp.sin(jnp.sqrt(k_n2) * jnp.dot(k_ij_n, r_ij))
            * jnp.dot(_epsilon, k_ij_n)
        )
        return _term_1

    return particle_mesh_ewald(_direct_sum_term, _reciprocal_sum_term)(r_ij, parameters)


@Partial
def translation_translational_periodic(r_ij, parameters):
    _dim = parameters.pbc.direct_lattice.shape[-1]
    a_i = a_j = radius = parameters.radius
    viscosity = parameters.viscosity
    _identity = jnp.eye(_dim)

    def _different_ij():
        r = jnp.linalg.norm(r_ij)
        _mobility = Mtt(r_ij, jnp.true_divide(a_i**2 + a_j**2, 2), parameters)
        return jax.lax.cond(
            r > a_i + a_j,
            lambda: _mobility,
            lambda: _mobility
            + Ytt(
                compute_nearest_image_lattice(r_ij, parameters.pbc),
                a_i,
                a_j,
                parameters,
            ),
        )

        # return Mtt(r_ij, jnp.true_divide(a_i**2 + a_j**2, 2), parameters) + Ytt(
        #     compute_nearest_image_lattice(r_ij, parameters.pbc),
        #     a_i,
        #     a_j,
        #     parameters,
        # )

    return jax.lax.cond(
        jnp.any(r_ij),
        _different_ij,
        lambda: (
            (
                jnp.reciprocal(6 * jnp.pi * viscosity * radius)
                + jnp.reciprocal(
                    4
                    * jnp.sqrt(2 * jnp.pi**3)
                    * parameters.splitting
                    * parameters.viscosity,
                )
                * (jnp.true_divide(radius**2, 9 * parameters.splitting**2) - 1)
            )
            * _identity
            + Mtt(jnp.zeros(_dim), radius, parameters)
        ),
    )


@Partial
def rotational_rotational_periodic(r_ij, parameters):
    _dim = parameters.pbc.direct_lattice.shape[-1]
    a_i = a_j = radius = parameters.radius
    viscosity = parameters.viscosity
    _identity = jnp.eye(_dim)

    def _different_ij():
        r = jnp.linalg.norm(r_ij)
        _mobility = Mrr(r_ij, parameters)
        return jax.lax.cond(
            r > a_i + a_j,
            lambda: _mobility,
            lambda: _mobility
            + Yrr(
                compute_nearest_image_lattice(r_ij, parameters.pbc),
                a_i,
                a_j,
                parameters,
            ),
        )
        # return Mrr(r_ij, parameters) + Yrr(
        #     compute_nearest_image_lattice(r_ij, parameters.pbc),
        #     a_i,
        #     a_j,
        #     parameters,
        # )

    return jax.lax.cond(
        jnp.any(r_ij),
        _different_ij,
        lambda: (
            (
                jnp.reciprocal(8.0 * jnp.pi * viscosity * radius**3)
                - jnp.reciprocal(
                    48
                    * jnp.sqrt(2 * jnp.pi**3)
                    * parameters.splitting**3
                    * parameters.viscosity
                )
            )
            * _identity
            + Mrr(jnp.zeros(_dim), parameters)
        ),
    )


@Partial
def rotational_translational_periodic(r_ij, parameters):
    _dim = parameters.pbc.direct_lattice.shape[-1]
    a_i = a_j = parameters.radius

    def _different_ij():
        r = jnp.linalg.norm(r_ij)
        _mobility = Mrt(r_ij, parameters)
        return jax.lax.cond(
            r > a_i + a_j,
            lambda: _mobility,
            lambda: _mobility
            + Yrt(
                compute_nearest_image_lattice(r_ij, parameters.pbc),
                a_i,
                a_j,
                parameters,
            ),
        )
        # return Mrt(r_ij, parameters) + Yrt(
        #     compute_nearest_image_lattice(r_ij, parameters.pbc),
        #     a_i,
        #     a_j,
        #     parameters,
        # )

    return jax.lax.cond(
        jnp.any(r_ij),
        _different_ij,
        lambda: jnp.zeros((_dim, _dim)),
    )


@Partial
def rpy_periodic(r_ij, parameters, mode=Partial(lambda: "translation")):
    if mode() == "translation":
        tensor = translation_translational_periodic(r_ij, parameters)

    else:
        coupling_tt = translation_translational_periodic(r_ij, parameters)
        coupling_rr = rotational_rotational_periodic(r_ij, parameters)
        coupling_rt = rotational_translational_periodic(r_ij, parameters)

        tensor = jnp.block([[coupling_tt, coupling_rt.T], [coupling_rt, coupling_rr]])

    return tensor
