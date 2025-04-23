""""""

__all__ = [
    # "BasisOptimizerOrdered",
    # "BasisOptimizerMinimizer",
    # "BasisOptimizerRank",
    # "BasisOptimizerSequential",
    "BasisOptimizer",
    "BasisOptimizerCombinatorial",
]


from functools import partial
from typing import Callable, Optional, Union

import jax
import jax.numpy as jnp
from jax import lax
from jax.scipy.optimize import OptimizeResults, minimize
from jax.tree_util import Partial
from multimethod import multimethod

from sfx.basis.parameters import ParameterGroup
from sfx.core.sfx_object import SFXGroup, SFXObject
from sfx.helpers.math import create_member_set, recombine_matrix, split_matrix
from sfx.inference.data import Data, DataGroup
from sfx.inference.inferrer.diffusion import DiffusionCoefficients
from sfx.inference.projector import TrajectoryIntegral
from sfx.inference.statistics import Statistics
from sfx.utils.console.progress_bar import ProgressBarScan

_einsum = Partial(jnp.einsum, precision=lax.Precision.HIGHEST)


class BasisCriterions(SFXGroup):
    """Base class for Basis criterions."""

    __slots__ = []

    def __init__(self, grp, gid=["nllh_", "bic__", "gbic_", "gbicp", "aic__", "gaic_"]):
        super().__init__(gid=gid, grp=grp)


class BasisOptimizer(SFXObject):
    __slots__ = [
        "inferrer",
        "coefficients",
        "diffusion_estimator",
    ]

    def __init__(
        self,
        inferrer,
        diffusion_estimator,
        *args,
        coefficients=None,
        **kwargs,
    ) -> None:
        self.inferrer = inferrer
        self.coefficients = coefficients
        self.diffusion_estimator = diffusion_estimator

    @multimethod
    def _compute_criterions_term(self, *_):
        """Computes the inverse diffusion and basis over the data."""
        ...

    @_compute_criterions_term.register
    def _(
        self,
        data: Data,
        parameters: ParameterGroup,
        *_: None,
    ) -> DataGroup:
        """Computes the inverse diffusion (constant) and basis over the data."""

        return self.inferrer.projector.trajectory_integral.sum(
            self.__cct_const,
            data,
            parameters=parameters,
            message="Computing Criterion Terms",
        )

    @_compute_criterions_term.register
    def _(
        self,
        data: Data,
        parameters: ParameterGroup,
        diffusion_parameters: ParameterGroup,
        *_: None,
    ) -> DataGroup:
        """Computes the inverse diffusion (constant) and basis over the data."""

        return self.inferrer.projector.trajectory_integral.sum(
            self.__cct_func,
            data,
            parameters=parameters,
            diffusion_parameters=diffusion_parameters,
            message="Computing Criterion Terms",
        )

    @partial(jax.jit, static_argnums=(0,))
    def __cct_const(
        self,
        data: Data,
        parameters: ParameterGroup,
    ) -> jax.Array:
        basis_values = self.inferrer.projector.basis(data, parameters).array
        # Temporary
        # basis = self.inferrer.projector.basis(data, parameters)
        # basis_values = self.inferrer._compute_bridge(basis, data, parameters, 10).array

        _, nbparticles, dof = basis_values.shape

        _diffusion = split_matrix(
            self.diffusion_estimator,
            dof,
            dof,
        )

        _inverse_diffusion = split_matrix(
            jnp.linalg.pinv(self.diffusion_estimator),
            dof,
            dof,
        )

        _z = _einsum(
            "ijmn,jn->im",
            _inverse_diffusion,
            self.inferrer.projector.projection_modifier(data.future_motions),
        )

        hessian = _einsum(
            "ai...m,ijmn,bj...n->iab",
            basis_values,
            _diffusion,
            basis_values,
        )

        information = -0.25 * hessian * data.timestep

        extra = 0.5 * _einsum(
            "i...m,ijmn,aj...n->ia",
            _z,
            _diffusion,
            basis_values,
        )

        residual_z_z = _einsum("im,im->i", _z, _z)

        residual_z_basis = -2 * _einsum(
            "im,bi...m->ib",
            _z,
            basis_values * data.timestep,
        )

        residual_basis_basis = _einsum(
            "ai...m,bi...m->iab",
            basis_values * data.timestep,
            basis_values * data.timestep,
        )

        # Covariance estimator
        Bn_zz = _einsum(
            "ai...m,im,jn,bj...n->iab",
            basis_values,
            _z,
            _z,
            basis_values,
        )

        Bn_zb = -(
            _einsum(
                "ai...m,im,cj...n,bj...n->iacb",
                basis_values,
                _z,
                basis_values * data.timestep,
                basis_values,
            )
            + _einsum(
                "ai...m,ci...m,jn,bj...n->iacb",
                basis_values,
                basis_values * data.timestep,
                _z,
                basis_values,
            )
        )

        Bn_bb = _einsum(
            "ai...m,ci...m,cj...n,bj...n->iacb",
            basis_values,
            basis_values * data.timestep,
            basis_values * data.timestep,
            basis_values,
        )

        total_dof = jnp.full(nbparticles, dof)

        # We skip the multiplication by nbparticles as it will be summed
        # using trajectory_integral.sum()
        constant = (
            # -0.5 * nbparticles * dof * jnp.log(4 * jnp.pi * data.timestep)
            -0.5 * dof * jnp.log(4 * jnp.pi * data.timestep)
            - 0.5
            * jnp.reciprocal(nbparticles)
            * jnp.log(jnp.linalg.det(recombine_matrix(_inverse_diffusion)))
            - 0.25
            * jnp.reciprocal(data.timestep)
            * _einsum("im,ijmn,jn->i", _z, _diffusion, _z)
        )

        return (
            total_dof,
            constant,
            information,
            extra,
            hessian,
            ####
            Bn_zz,
            Bn_zb,
            Bn_bb,
            ####
            residual_z_z,
            residual_z_basis,
            residual_basis_basis,
            ####
        )

    @partial(jax.jit, static_argnums=(0,))
    def __cct_func(
        self,
        data: Data,
        parameters: ParameterGroup,
        diffusion_parameters: ParameterGroup,
    ) -> jax.Array:
        basis_values = self.inferrer.projector.basis(data, parameters).array

        _, nbparticles, dof = basis_values.shape

        _diffusion = self.diffusion_estimator(data, diffusion_parameters).array[0]
        _inverse_diffusion = split_matrix(
            jnp.linalg.pinv(recombine_matrix(_diffusion)),
            dof,
            dof,
        )

        _z = _einsum(
            "ijmn,jn->im",
            _inverse_diffusion,
            self.inferrer.projector.projection_modifier(data.future_motions),
        )

        hessian = _einsum(
            "ai...m,ijmn,bj...n->iab",
            basis_values,
            _diffusion,
            basis_values,
        )

        information = -0.25 * hessian * data.timestep

        extra = 0.5 * _einsum(
            "i...m,ijmn,aj...n->ia",
            _z,
            _diffusion,
            basis_values,
        )

        residual_z_z = _einsum("im,im->i", _z, _z)

        residual_z_basis = -2 * _einsum(
            "im,bi...m->ib",
            _z,
            basis_values * data.timestep,
        )

        residual_basis_basis = _einsum(
            "ai...m,bi...m->iab",
            basis_values * data.timestep,
            basis_values * data.timestep,
        )

        # Covariance estimator
        Bn_zz = _einsum(
            "ai...m,im,jn,bj...n->iab",
            basis_values,
            _z,
            _z,
            basis_values,
        )

        Bn_zb = -(
            _einsum(
                "ai...m,im,cj...n,bj...n->iacb",
                basis_values,
                _z,
                basis_values * data.timestep,
                basis_values,
            )
            + _einsum(
                "ai...m,ci...m,jn,bj...n->iacb",
                basis_values,
                basis_values * data.timestep,
                _z,
                basis_values,
            )
        )

        Bn_bb = _einsum(
            "ai...m,ci...m,cj...n,bj...n->iacb",
            basis_values,
            basis_values * data.timestep,
            basis_values * data.timestep,
            basis_values,
        )

        total_dof = jnp.full(nbparticles, dof)

        # We skip the multiplication by nbparticles as it will be summed
        # using trajectory_integral.sum()
        constant = (
            # -0.5 * nbparticles * dof * jnp.log(4 * jnp.pi * data.timestep)
            -0.5 * dof * jnp.log(4 * jnp.pi * data.timestep)
            - 0.5
            * jnp.reciprocal(nbparticles)
            * jnp.log(jnp.linalg.det(recombine_matrix(_inverse_diffusion)))
            - 0.25
            * jnp.reciprocal(data.timestep)
            * _einsum("im,ijmn,jn->i", _z, _diffusion, _z)
        )

        return (
            total_dof,
            constant,
            information,
            extra,
            hessian,
            ####
            Bn_zz,
            Bn_zb,
            Bn_bb,
            ####
            residual_z_z,
            residual_z_basis,
            residual_basis_basis,
            ####
        )


class BasisOptimizerCombinatorial(BasisOptimizer):
    """Finds the optimal basis."""

    __slots__ = [
        "costs",
        "combinations",
    ]

    def __init__(
        self,
        inferrer,
        diffusion_estimator,
        *args,
        costs=None,
        combinations=None,
        **kwargs,
    ) -> None:
        super().__init__(inferrer, diffusion_estimator, *args, **kwargs)
        self.costs = costs
        self.combinations = combinations

    def __call__(
        self,
        data: Data,
        parameters: ParameterGroup,
        diffusion_parameters: Optional[ParameterGroup] = None,
        diffusion_coefficients: Optional[DiffusionCoefficients] = None,
    ):
        # Get the number of parameters per group
        nbparameters = tuple(param[0] for param in parameters.shape[1])
        _terms = self._compute_criterions_term(
            data,
            parameters,
            diffusion_parameters,
            diffusion_coefficients,
        )

        self.costs, self.combinations = self._optimize(nbparameters, _terms)

        self.coefficients = self.inferrer.projector.trajectory_integral.map(
            lambda _, comb, coeff, mat: type(self.inferrer.coefficients)(
                BasisCriterions(
                    [
                        self._compute_coefficients(nbparameters, c, coeff, mat)
                        for c in comb.array
                    ]
                )
            ),
            self.combinations,
            self.inferrer.coefficients.drift,
            self.inferrer.orthonormalization_matrix,
        )

        return

    @partial(jax.jit, static_argnums=(0, 1))
    def _optimize(self, nbparameters, terms):
        total_nbparameters = sum(nbparameters)
        combinations, cardinality = create_member_set(
            jnp.asarray([0, 1]),
            total_nbparameters,
        )
        nbcombinations = len(combinations)

        @ProgressBarScan(nbcombinations, message="Computing Criterions")
        def _compute_criterions_combinations(carry, xs):
            coefficients, matrix, terms = carry
            (combination,) = xs
            return (
                carry,
                self._test_bases(
                    terms,
                    nbparameters,
                    matrix,
                    coefficients,
                    combination,
                ),
            )

        _array = self.inferrer.projector.trajectory_integral.map(
            lambda _, coeff, matrix, *terms: jax.lax.scan(
                _compute_criterions_combinations,
                (coeff, matrix, terms),
                (jnp.arange(nbcombinations), combinations),
            )[-1],
            self.inferrer.coefficients.drift,
            self.inferrer.orthonormalization_matrix,
            *terms,
        )

        minimums = self.inferrer.projector.trajectory_integral.map(
            lambda _, arr: BasisCriterions(
                jax.lax.fori_loop(
                    0,
                    total_nbparameters,
                    lambda i, v: v.at[i].set(
                        jnp.nanmin(
                            jnp.where(
                                i == cardinality[..., jnp.newaxis],
                                arr,
                                jnp.nan,
                            ),
                            axis=0,
                        )
                    ),
                    jnp.zeros((total_nbparameters, arr.shape[-1])),
                ).T,
            ),
            _array,
        )

        best_combinations = self.inferrer.projector.trajectory_integral.map(
            lambda _, arr: BasisCriterions(combinations[jnp.nanargmin(arr, axis=0)]),
            _array,
        )

        return minimums, best_combinations

    @partial(jax.jit, static_argnums=(0, 2))
    def _test_bases(self, terms, nbparameters, matrix, coefficients, combination):
        select = jnp.outer(combination, combination)

        matrix_arr = matrix.array
        coeff_arr = coefficients.array

        _selected_matrix = select * matrix_arr
        _selected_hessian = select * terms[4]
        invA = jnp.zeros_like(matrix_arr)
        inv_hessian = jnp.zeros_like(matrix_arr)

        _offset = 0
        for i in nbparameters:
            _end = _offset + i
            invA = invA.at[_offset:_end, _offset:_end].set(
                jnp.linalg.pinv(_selected_matrix[_offset:_end, _offset:_end])
            )
            inv_hessian = inv_hessian.at[_offset:_end, _offset:_end].set(
                jnp.linalg.pinv(_selected_hessian[_offset:_end, _offset:_end])
            )

            _offset += i

        # invA = jnp.linalg.pinv(_selected_matrix)
        # inv_hessian = jnp.linalg.pinv(select * terms[4])
        orthonormalized_coefficients = jnp.matmul(invA, coeff_arr)
        n = terms[0]
        b = jnp.sum(combination)

        information = _einsum(
            "a,b,ab",
            orthonormalized_coefficients,
            orthonormalized_coefficients,
            terms[2],
        )

        extra = _einsum(
            "a,a",
            orthonormalized_coefficients,
            terms[3],
        )

        inv_residual2 = jnp.reciprocal(
            terms[8]
            + _einsum(
                "a,a",
                orthonormalized_coefficients,
                terms[9],
            )
            + _einsum(
                "a,b,ab",
                orthonormalized_coefficients,
                orthonormalized_coefficients,
                terms[10],
            )
        )

        Bn = (
            _einsum(
                "ab,a,b->ab",
                terms[5],
                combination,
                combination,
            )
            + _einsum(
                "c,acb,a,b->ab",
                orthonormalized_coefficients,
                terms[6],
                combination,
                combination,
            )
            + _einsum(
                "c,acb,a,b->ab",
                orthonormalized_coefficients**2,
                terms[7],
                combination,
                combination,
            )
        )

        Hn_trace = (n - b) * inv_residual2 * (inv_hessian @ Bn)

        Hn_det = (
            (n - b)
            * inv_residual2
            * (
                inv_hessian @ Bn
                + jnp.where(
                    jnp.diag(jnp.logical_not(combination)),
                    1.0,
                    0.0,
                )
            )
        )

        nllh = -terms[1] - information - extra
        aic = 2 * nllh + 2 * b
        bic = 2 * nllh + jnp.log(n) * b

        logdetH = jnp.log(jnp.linalg.det(Hn_det))
        trH = jnp.trace(Hn_trace)

        gbic = bic - logdetH
        gbicp = gbic + trH
        gaic = 2 * nllh + 2 * trH

        return jnp.asarray(
            [
                nllh,
                bic,
                gbic,
                gbicp,
                aic,
                gaic,
            ]
        )

    @partial(jax.jit, static_argnums=(0, 1))
    def _compute_coefficients(self, nbparameters, combination, coeff, mat):
        coefficients = jnp.zeros_like(coeff.array)

        _select = jnp.outer(combination, combination)
        _start = 0

        for nb in nbparameters:
            _end = _start + nb
            _mask = _select[_start:_end, _start:_end]
            inv_matrix = jnp.linalg.pinv(_mask * mat.array[_start:_end, _start:_end])
            coefficients = coefficients.at[_start:_end].set(
                jnp.matmul(inv_matrix, coeff.array[_start:_end])
            )
            _start += _end

        return coeff.regroup(coefficients)


class _BasisOptimizer(SFXObject):
    __slots__ = [
        "inferrer",
        "coefficients",
        "diffusion_estimator",
    ]

    def __init__(
        self,
        inferrer,
        diffusion_estimator,
        *args,
        coefficients=None,
        **kwargs,
    ) -> None:
        self.inferrer = inferrer
        self.coefficients = coefficients
        self.diffusion_estimator = diffusion_estimator

    def _compute_criterions_term(
        self,
        data: Data,
        parameters: ParameterGroup,
        *_: None,
    ) -> DataGroup:
        """Computes the inverse diffusion (constant) and basis over the data."""

        nbfunctions = self.inferrer.orthonormalization_matrix[-1][-1].shape[-1]
        _initial_carry = (
            (
                0,
                0.0,
                jnp.zeros((nbfunctions, nbfunctions)),
                jnp.zeros((nbfunctions,)),
                jnp.zeros((nbfunctions, nbfunctions)),
                ###
                jnp.zeros((nbfunctions, nbfunctions)),
                jnp.zeros((nbfunctions, nbfunctions, nbfunctions)),
                jnp.zeros((nbfunctions, nbfunctions, nbfunctions)),
                ###
                0.0,
                jnp.zeros((nbfunctions,)),
                jnp.zeros((nbfunctions, nbfunctions)),
            ),
            parameters,
        )

        _length = len(data)
        _nbterms = len(_initial_carry[0])

        @ProgressBarScan(
            len(data),
            message="Computing Criterion Terms",
            tqdm_options={"leave": True},
        )
        def _compute(carry, xs):
            (data,) = xs
            loglikelihood, parameters = carry
            terms = self.__cct_const(data, parameters)
            return (
                (
                    tuple(loglikelihood[i] + terms[i] for i in range(_nbterms)),
                    parameters,
                ),
                None,
            )

        return jax.lax.scan(
            _compute,
            _initial_carry,
            (jnp.arange(_length), data),
        )[
            0
        ][0]

    @partial(jax.jit, static_argnums=(0,))
    def __cct_const(
        self,
        data: Data,
        parameters: ParameterGroup,
    ) -> jax.Array:
        basis_values = self.inferrer.projector.basis(data, parameters).array

        nbfunctions, nbparticles, dof = basis_values.shape

        _diffusion = split_matrix(
            self.diffusion_estimator,
            dof,
            dof,
        )

        _inverse_diffusion = split_matrix(
            jnp.linalg.pinv(self.diffusion_estimator),
            dof,
            dof,
        )

        _z = _einsum(
            "ijmn,jn->im",
            _inverse_diffusion,
            self.inferrer.projector.projection_modifier(data.future_motions),
        )

        hessian = _einsum(
            "ai...m,ijmn,bj...n->ab",
            basis_values,
            _diffusion,
            basis_values,
        )

        information = -0.25 * hessian * data.timestep

        extra = 0.5 * _einsum(
            "i...m,ijmn,aj...n->a",
            _z,
            _diffusion,
            basis_values,
        )

        residual_z_z = _einsum("im,im", _z, _z)

        residual_z_basis = -2 * _einsum(
            "im,bi...m->b",
            _z,
            basis_values * data.timestep,
        )

        residual_basis_basis = _einsum(
            "ai...m,bi...m->ab",
            basis_values * data.timestep,
            basis_values * data.timestep,
        )

        # Covariance estimator
        Bn_zz = _einsum(
            "ai...m,im,jn,bj...n->ab",
            basis_values,
            _z,
            _z,
            basis_values,
        )

        Bn_zb = -(
            _einsum(
                "ai...m,im,cj...n,bj...n->acb",
                basis_values,
                _z,
                basis_values * data.timestep,
                basis_values,
            )
            + _einsum(
                "ai...m,ci...m,jn,bj...n->acb",
                basis_values,
                basis_values * data.timestep,
                _z,
                basis_values,
            )
        )

        Bn_bb = _einsum(
            "ai...m,ci...m,cj...n,bj...n->acb",
            basis_values,
            basis_values * data.timestep,
            basis_values * data.timestep,
            basis_values,
        )

        total_dof = nbparticles * dof
        constant = (
            -0.5 * nbparticles * dof * jnp.log(4 * jnp.pi * data.timestep)
            - 0.5 * jnp.log(jnp.linalg.det(recombine_matrix(_inverse_diffusion)))
            - 0.25
            * jnp.reciprocal(data.timestep)
            * _einsum("im,ijmn,jn", _z, _diffusion, _z)
        )

        return (
            total_dof,
            constant,
            information,
            extra,
            hessian,
            ####
            Bn_zz,
            Bn_zb,
            Bn_bb,
            ####
            residual_z_z,
            residual_z_basis,
            residual_basis_basis,
            ####
        )


class _BasisOptimizerCombinatorial(_BasisOptimizer):
    """Finds the optimal basis."""

    __slots__ = [
        "costs",
        "combinations",
    ]

    def __init__(
        self,
        inferrer,
        diffusion_estimator,
        *args,
        costs=None,
        combinations=None,
        **kwargs,
    ) -> None:
        super().__init__(inferrer, diffusion_estimator, *args, **kwargs)
        self.costs = costs
        self.combinations = combinations

    def __call__(
        self,
        data: Data,
        parameters: ParameterGroup,
        diffusion_parameters: Optional[ParameterGroup] = None,
        diffusion_coefficients: Optional[DiffusionCoefficients] = None,
        temporal_group=None,
        particle_group=None,
    ):
        _terms = self._compute_criterions_term(data, parameters)

        # Get the number of parameters per group
        nbparameters = tuple(param[0] for param in parameters.shape[1])
        self.costs, self.combinations = self._optimize(
            _terms,
            nbparameters,
            temporal_group,
            particle_group,
        )

        self.coefficients = jax.lax.scan(
            lambda _, c: (
                _,
                jnp.matmul(
                    jnp.linalg.pinv(
                        jnp.outer(c, c)
                        * self.inferrer.orthonormalization_matrix[temporal_group][
                            particle_group
                        ].array
                    ),
                    self.inferrer.coefficients.drift[temporal_group][
                        particle_group
                    ].array,
                ),
            ),
            None,
            self.combinations,
        )[-1]

        return

    @partial(jax.jit, static_argnums=(0, 2, 3, 4))
    def _optimize(self, terms, nbparameters, tg, pg):
        _nbfuncs = self.inferrer.orthonormalization_matrix[tg][pg].shape[-1]
        combinations, cardinality = create_member_set(
            jnp.asarray([0, 1]),
            _nbfuncs,
        )

        # nllh, bic, gbic, gbicp, aic, gaic
        _array = jax.lax.scan(
            ProgressBarScan(
                len(combinations),
                message="Computing Criterions",
            )(
                lambda _, xs: (
                    _,
                    self._test_bases(
                        terms,
                        nbparameters,
                        self.inferrer.orthonormalization_matrix[tg][pg].array,
                        self.inferrer.coefficients.drift[tg][pg].array,
                        xs[0],
                    ),
                )
            ),
            None,
            (jnp.arange(len(combinations)), combinations),
        )[-1]

        _min = jax.lax.fori_loop(
            0,
            _nbfuncs,
            lambda i, v: v.at[i].set(
                jnp.nanmin(
                    jnp.where(
                        i == cardinality[..., jnp.newaxis],
                        _array,
                        jnp.nan,
                    ),
                    axis=0,
                )
            ),
            jnp.zeros((_nbfuncs, _array.shape[-1])),
        ).T

        return _min, combinations[jnp.nanargmin(_array, axis=0)]

    @partial(jax.jit, static_argnums=(0, 2))
    def _test_bases(self, terms, nbparameters, matrix, coefficients, combination):
        select = jnp.outer(combination, combination)

        _selected_matrix = select * matrix
        _selected_hessian = select * terms[4]
        invA = jnp.zeros_like(matrix)
        inv_hessian = jnp.zeros_like(matrix)

        _offset = 0
        for i in nbparameters:
            _end = _offset + i
            invA = invA.at[_offset:_end, _offset:_end].set(
                jnp.linalg.pinv(_selected_matrix[_offset:_end, _offset:_end])
            )
            inv_hessian = inv_hessian.at[_offset:_end, _offset:_end].set(
                jnp.linalg.pinv(_selected_hessian[_offset:_end, _offset:_end])
            )

            _offset += i

        # invA = jnp.linalg.pinv(_selected_matrix)
        # inv_hessian = jnp.linalg.pinv(select * terms[4])
        orthonormalized_coefficients = jnp.matmul(invA, coefficients)
        n = terms[0]
        b = jnp.sum(combination)

        information = _einsum(
            "a,b,ab",
            orthonormalized_coefficients,
            orthonormalized_coefficients,
            terms[2],
        )

        extra = _einsum(
            "a,a",
            orthonormalized_coefficients,
            terms[3],
        )

        inv_residual2 = jnp.reciprocal(
            terms[8]
            + _einsum(
                "a,a",
                orthonormalized_coefficients,
                terms[9],
            )
            + _einsum(
                "a,b,ab",
                orthonormalized_coefficients,
                orthonormalized_coefficients,
                terms[10],
            )
        )

        Bn = (
            _einsum(
                "ab,a,b->ab",
                terms[5],
                combination,
                combination,
            )
            + _einsum(
                "c,acb,a,b->ab",
                orthonormalized_coefficients,
                terms[6],
                combination,
                combination,
            )
            + _einsum(
                "c,acb,a,b->ab",
                orthonormalized_coefficients**2,
                terms[7],
                combination,
                combination,
            )
        )

        Hn_trace = (n - b) * inv_residual2 * (inv_hessian @ Bn)

        Hn_det = (
            (n - b)
            * inv_residual2
            * (
                inv_hessian @ Bn
                + jnp.where(
                    jnp.diag(jnp.logical_not(combination)),
                    1.0,
                    0.0,
                )
            )
        )

        nllh = -terms[1] - information - extra
        aic = 2 * nllh + 2 * b
        bic = 2 * nllh + jnp.log(n) * b

        logdetH = jnp.log(jnp.linalg.det(Hn_det))
        trH = jnp.trace(Hn_trace)

        gbic = bic - logdetH
        gbicp = gbic + trH
        gaic = 2 * nllh + 2 * trH

        return jnp.asarray(
            [
                nllh,
                bic,
                gbic,
                gbicp,
                aic,
                gaic,
            ]
        )


'''
class BasisOptimizer(SFXObject):
    __slots__ = ["inferrer", "coefficients", "diffusion_estimator", "cost", "error"]

    def __init__(
        self,
        inferrer,
        diffusion_estimator,
        *args,
        cost=Partial(lambda info: info.mean - info.bias - 2 * info.error),
        coefficients=None,
        error=None,
        **kwargs,
    ) -> None:
        self.inferrer = inferrer
        self.coefficients = coefficients
        self.diffusion_estimator = diffusion_estimator
        self.cost = cost
        self.error = error

    @multimethod
    def _compute_information(self, *_):
        """Computes the inverse diffusion and basis over the data."""
        ...

    @_compute_information.register
    def _(
        self,
        data: Data,
        parameters: ParameterGroup,
        *_: None,
    ) -> DataGroup:
        """Computes the inverse diffusion (constant) and basis over the data."""

        return self.inferrer.projector.trajectory_integral.integrate(
            self.__cli_const,
            data,
            parameters=parameters,
            message="Computing information",
        )

    @_compute_information.register
    def _(
        self,
        data: Data,
        parameters: ParameterGroup,
        diffusion_parameters: ParameterGroup,
        *_: None,
    ) -> DataGroup:
        """Computes the inverse diffusion (function) and basis over the data."""

        return self.inferrer.projector.trajectory_integral.integrate(
            self.__cli_func,
            data,
            parameters=parameters,
            diffusion_parameters=diffusion_parameters,
            message="Computing information",
        )

    @_compute_information.register
    def _(
        self,
        data: Data,
        parameters: ParameterGroup,
        diffusion_parameters: ParameterGroup,
        diffusion_coefficients: DiffusionCoefficients,
    ) -> DataGroup:
        """Computes the inverse diffusion (ansatz) and basis over the data."""

        return self.inferrer.projector.trajectory_integral.map(
            lambda ti, coeff, params, diff_params: ti.integrate(
                self.__cli_ansatz,
                data,
                diffusion_coefficients=coeff,
                parameters=params,
                diffusion_parameters=diff_params,
                message="Computing information",
            ).array[0],
            diffusion_coefficients.diffusion,
            params=parameters,
            diff_params=diffusion_parameters,
        )

    @partial(jax.jit, static_argnums=(0,))
    def __cli_ansatz(
        self,
        data: Data,
        diffusion_coefficients: DiffusionCoefficients,
        parameters: ParameterGroup,
        diffusion_parameters: ParameterGroup,
    ) -> jax.Array:
        basis_values = self.inferrer.projector.basis(data, parameters).array

        inverse_diffusion = split_matrix(
            jnp.linalg.pinv(
                recombine_matrix(
                    self.diffusion_estimator(
                        data,
                        diffusion_parameters,
                        diffusion_coefficients,
                    )
                )
            ),
            data.coordinates.dof,
            data.coordinates.dof,
        )

        capacity = 0.5 * jnp.einsum(
            "ijmn,ai...m,bj...n->iab",
            inverse_diffusion,
            basis_values,
            basis_values,
            precision=lax.Precision.HIGHEST,
        )

        return capacity

    @partial(jax.jit, static_argnums=(0,))
    def __cli_func(
        self,
        data: Data,
        parameters: ParameterGroup,
        diffusion_parameters: ParameterGroup,
    ) -> jax.Array:
        basis_values = self.inferrer.projector.basis(data, parameters).array

        inverse_diffusion = split_matrix(
            jnp.linalg.pinv(
                recombine_matrix(self.diffusion_estimator(data, diffusion_parameters))
            ),
            data.coordinates.dof,
            data.coordinates.dof,
        )

        capacity = 0.5 * jnp.einsum(
            "ijmn,ai...m,bj...n->iab",
            inverse_diffusion,
            basis_values,
            basis_values,
            precision=lax.Precision.HIGHEST,
        )

        return capacity

    @partial(jax.jit, static_argnums=(0,))
    def __cli_const(
        self,
        data: Data,
        parameters: ParameterGroup,
    ) -> jax.Array:
        basis_values = self.inferrer.projector.basis(data, parameters).array

        inverse_diffusion = split_matrix(
            jnp.linalg.pinv(recombine_matrix(self.diffusion_estimator)),
            data.coordinates.dof,
            data.coordinates.dof,
        )

        capacity = 0.5 * jnp.einsum(
            "ijmn,ai...m,bj...n->iab",
            inverse_diffusion,
            basis_values,
            basis_values,
            precision=lax.Precision.HIGHEST,
        )

        return capacity


class BasisOptimizerOrdered(BasisOptimizer):
    """Finds the optimal basis."""

    __slots__ = [
        "information_evolution",
        "nbfunctions",
    ]

    def __init__(
        self,
        inferrer,
        diffusion_estimator,
        *args,
        information_evolution=None,
        nbfunctions=None,
        **kwargs,
    ) -> None:
        super().__init__(inferrer, diffusion_estimator, *args, **kwargs)
        self.information_evolution = information_evolution
        self.nbfunctions = nbfunctions

    def __call__(
        self,
        data: Data,
        parameters: ParameterGroup,
        diffusion_parameters: Optional[ParameterGroup] = None,
        diffusion_coefficients: Optional[DiffusionCoefficients] = None,
    ):
        information = self._compute_information(
            data,
            parameters,
            diffusion_parameters,
            diffusion_coefficients,
        )

        self.information_evolution = self._optimize(information)

        self.nbfunctions = self.information_evolution.map(
            lambda node: self._get_best_basis(node)
        )

        self.coefficients = self.inferrer.projector.trajectory_integral.map(
            lambda _, coeff, matrix, best: coeff.regroup(
                jnp.matmul(
                    jnp.linalg.pinv(
                        matrix.array
                        * jnp.outer(
                            jnp.zeros(coeff.shape).at[: best[0]].set(1.0),
                            jnp.zeros(coeff.shape).at[: best[0]].set(1.0),
                        )
                    ),
                    coeff.array,
                )
            ),
            self.inferrer.coefficients.drift,
            self.inferrer.orthonormalization_matrix,
            self.nbfunctions,
        )

    @partial(jax.jit, static_argnums=(0,))
    def _get_best_basis(self, information):
        # corrected_information = (
        #    information.mean - information.bias - 2 * information.error
        # )
        cost = self.cost(information)
        index = jnp.argmax(cost)
        return index, cost[index]

    @partial(jax.jit, static_argnums=(0,))
    def _optimize(self, information):
        results = self.inferrer.projector.trajectory_integral.map(
            lambda _, info, coeff, mat: self._test_bases(info, coeff, mat),
            information,
            self.inferrer.coefficients.drift,
            self.inferrer.orthonormalization_matrix,
        )

        return results

    @partial(jax.jit, static_argnums=(0,))
    def _test_bases(
        self,
        information,
        coefficients,
        matrix,
    ):
        masks = jnp.tri(*matrix.array.shape, dtype=jnp.bool_)

        @ProgressBarScan(
            len(masks),
            message="Computing information for ordered basis combinations.",
        )
        def _compute_information_combination(_, x):
            (mask,) = x
            select = jnp.outer(mask, mask)
            orthonormalized_coefficients = jnp.matmul(
                jnp.linalg.pinv(select * matrix.array),
                coefficients.array,
            )

            mean = jnp.einsum(
                "a,b,ab",
                orthonormalized_coefficients,
                orthonormalized_coefficients,
                information,
                precision=lax.Precision.HIGHEST,
            )

            bias = 0.5 * jnp.count_nonzero(mask)

            error = jnp.sqrt(2 * mean + 0.25 * (jnp.count_nonzero(mask)) ** 2)

            return (None, Statistics(mean=mean, bias=bias, error=error))

        information_evolution = jax.lax.scan(
            _compute_information_combination,
            None,
            (jnp.arange(len(masks)), masks),
        )[-1]

        return information_evolution


class BasisOptimizerSequential(BasisOptimizer):
    """Finds the optimal basis."""

    __slots__ = [
        "best_information",
        "mask",
    ]

    def __init__(
        self,
        inferrer,
        diffusion_estimator,
        *args,
        best_information=None,
        mask=None,
        **kwargs,
    ) -> None:
        super().__init__(inferrer, diffusion_estimator, *args, **kwargs)
        self.best_information = best_information
        self.mask = mask

    def __call__(
        self,
        data: Data,
        parameters: ParameterGroup,
        diffusion_parameters: Optional[ParameterGroup] = None,
        diffusion_coefficients: Optional[DiffusionCoefficients] = None,
    ):
        information = self._compute_information(
            data,
            parameters,
            diffusion_parameters,
            diffusion_coefficients,
        )

        optimization_result = self._optimize(information)
        self.mask = optimization_result.map(lambda node: node[0])
        self.best_information = optimization_result.map(lambda node: node[-1])

        self.coefficients = self.inferrer.projector.trajectory_integral.map(
            lambda _, mask, matrix, coefficient: coefficient.regroup(
                jnp.matmul(
                    jnp.linalg.pinv(jnp.outer(mask, mask) * matrix.array),
                    mask * coefficient.array,
                    precision=lax.Precision.HIGHEST,
                )
            ),
            self.mask,
            self.inferrer.orthonormalization_matrix,
            self.inferrer.coefficients.drift,
        )

    @partial(jax.jit, static_argnums=(0,))
    def _optimize(self, information):
        results = self.inferrer.projector.trajectory_integral.map(
            lambda _, info, coeff, mat: self._test_bases(info, coeff, mat),
            information,
            self.inferrer.coefficients.drift,
            self.inferrer.orthonormalization_matrix,
        )

        return results

    @partial(jax.jit, static_argnums=(0,))
    def _test_bases(
        self,
        information,
        coefficients,
        matrix,
    ):
        def _compute_information(mask):
            select = jnp.outer(mask, mask)
            orthonormalized_coefficients = jnp.matmul(
                jnp.linalg.pinv(select * matrix.array),
                coefficients.array,
            )

            new_information = jnp.einsum(
                "a,b,ab",
                orthonormalized_coefficients,
                orthonormalized_coefficients,
                information,
                precision=lax.Precision.HIGHEST,
            )

            return new_information

        def _false_fun(i, mask, _):
            new_mask = mask.at[i].set(True)
            return (new_mask, _compute_information(new_mask))

        def _true_fun(_, mask, info):
            return (mask, info)

        def _fori_loop_body(i, val):
            mask, info, masks, current_info = val

            new_mask, new_info = jax.lax.cond(
                mask[i],
                _true_fun,
                _false_fun,
                i,
                mask,
                current_info,
            )

            return (
                mask,
                info.at[i].set(new_info),
                masks.at[i].set(new_mask),
                current_info,
            )

        def _while_loop_body(carry):
            mask, info = carry

            _, info_masks, masks, _ = jax.lax.fori_loop(
                0,
                mask.shape[0],
                _fori_loop_body,
                (
                    mask,
                    jnp.zeros(mask.shape[0]),
                    jnp.zeros((mask.shape[0], mask.shape[0]), dtype=jnp.bool_),
                    info[-1],
                ),
            )
            index = jnp.argmax(info_masks)
            new_mask = masks[index]
            new_info = info_masks[index]
            return (
                new_mask,
                info.at[0].set(info[-1]).at[1].set(new_info),
            )

        def _while_loop_cond(carry):
            _, info = carry
            diff = jnp.diff(info)[0]
            return jnp.logical_or(
                diff > 0,
                jnp.isnan(diff),
            )

        mask, info = jax.lax.while_loop(
            _while_loop_cond,
            _while_loop_body,
            (
                jnp.zeros_like(coefficients.array, dtype=jnp.bool_),
                jnp.asarray([-jnp.inf, -jnp.inf]),
            ),
        )

        bias = 0.5 * jnp.count_nonzero(mask)
        error = jnp.sqrt(2 * info[-1] + 0.25 * (jnp.count_nonzero(mask)) ** 2)

        return (mask, Statistics(mean=info[-1], bias=bias, error=error))


class BasisOptimizerMinimizer(BasisOptimizer):
    """Finds the optimal basis."""

    __slots__ = [
        "activation",
    ]

    def __init__(
        self,
        inferrer,
        *args,
        diffusion_estimator,
        activation=None,
        **kwargs,
    ) -> None:
        super().__init__(inferrer, diffusion_estimator, *args, **kwargs)
        self.activation = activation

    def __call__(
        self,
        data: Data,
        parameters: ParameterGroup,
        diffusion_parameters: Optional[ParameterGroup] = None,
        diffusion_coefficients: Optional[DiffusionCoefficients] = None,
    ):
        information = self._compute_information(
            data,
            parameters,
            diffusion_parameters,
            diffusion_coefficients,
        )

        optimization_result = self._optimize_coefficients(information)

        self.activation = optimization_result.map(
            lambda node: self.activation_function(node.x),
            lambda node: isinstance(node, OptimizeResults),
        )

        self.coefficients = self.inferrer.projector.trajectory_integral.map(
            lambda _, activation, matrix, coefficient: coefficient.regroup(
                jnp.matmul(
                    jnp.linalg.pinv(jnp.outer(activation, activation) * matrix.array),
                    activation * coefficient.array,
                    precision=lax.Precision.HIGHEST,
                )
            ),
            self.activation,
            self.inferrer.orthonormalization_matrix,
            self.inferrer.coefficients.drift,
        )

    @partial(jax.jit, static_argnums=(0,))
    def _optimize_coefficients(self, information):
        results = self.inferrer.projector.trajectory_integral.map(
            lambda _, info, coeff, matrix: self._minimize(info, coeff, matrix),
            information,
            self.inferrer.coefficients.drift,
            self.inferrer.orthonormalization_matrix,
        )

        return results

    @partial(jax.jit, static_argnums=(0,))
    def _minimize(
        self,
        information,
        coefficients,
        matrix,
    ):
        params = jnp.zeros_like(coefficients.array)

        result = minimize(
            self._minimizer,
            params,
            args=(
                information,
                coefficients.array,
                matrix.array,
            ),
            method="BFGS",
        )

        return result

    @partial(jax.jit, static_argnums=(0,))
    def _minimizer(
        self,
        params,
        information,
        coefficients,
        matrix,
    ):
        activation = self.activation_function(params)

        orthonormalized_coefficients = jnp.matmul(
            jnp.linalg.pinv(jnp.outer(activation, activation) * matrix),
            coefficients,
        )

        mean = jnp.einsum(
            "a,b,ab",
            orthonormalized_coefficients,
            orthonormalized_coefficients,
            information,
            precision=lax.Precision.HIGHEST,
        )

        bias = 0.5 * jnp.sum(activation)
        error = jnp.sqrt(2 * mean + 0.25 * jnp.sum(activation) ** 2)

        return -self.cost(
            Statistics(mean=mean, bias=bias, error=error)
        )  # mean - bias - 2.0 * error)

    @partial(jax.jit, static_argnums=(0,))
    def activation_function(self, x):
        return jax.nn.hard_sigmoid(x)


class BasisOptimizerRank(BasisOptimizer):
    """Finds the optimal basis."""

    __slots__ = ["rank"]

    def __init__(
        self,
        inferrer,
        diffusion_estimator,
        *args,
        rank=None,
        **kwargs,
    ) -> None:
        super().__init__(
            inferrer,
            diffusion_estimator,
            *args,
            **kwargs,
        )
        self.rank = rank

    def __call__(self):
        self.rank = self.inferrer.projector.trajectory_integral.map(
            lambda _, matrix: jnp.linalg.matrix_rank(matrix.array),
            self.inferrer.orthonormalization_matrix,
        )

        self.coefficients = self.inferrer.projector.trajectory_integral.map(
            lambda _, rank, matrix, coeff: coeff.regroup(
                self._keep_max_response(rank, matrix, coeff),
            ),
            self.rank,
            self.inferrer.orthonormalization_matrix,
            self.inferrer.coefficients.drift,
        )

    def _keep_max_response(self, rank, matrix, coefficients):
        matrix_array = matrix.array
        coefficients_array = coefficients.array

        response = jnp.diag(jnp.linalg.pinv(matrix_array) @ matrix_array)
        indices = jnp.argsort(response)[::-1][:rank]
        mask = jnp.zeros(coefficients_array.shape).at[indices].set(1.0)

        return jnp.matmul(
            jnp.linalg.pinv(matrix_array * jnp.outer(mask, mask)),
            coefficients_array,
        )
'''
