__all__ = [
    "ForceInferrer",
]

from collections.abc import Callable
from functools import partial
from typing import Optional, Tuple

import jax
import jax.numpy as jnp
import jax.scipy as jsp
from jax.tree_util import Partial

from sfx.basis.parameters import ParameterGroup
from sfx.helpers.math import (
    binomial_coefficient,
    create_member_set,
    group_iterative_mgs,
    split_matrix,
)
from sfx.inference.data import Data, DataGroup
from sfx.inference.inferrer.core import (
    Coefficients,
    InferenceOptions,
    Inferrer,
    Projections,
    MultiModelSelection,
)
from sfx.inference.projector import Projector, ProjectorGMGS
from sfx.utils.console.progress_bar import ProgressBarScan
import sfx.helpers.sharding as shs

_einsum = Partial(jnp.einsum, precision=jax.lax.Precision.HIGHEST)


class ForceCoefficients(Coefficients):
    """Force coefficients class."""

    __slots__ = ["force"]

    def __init__(
        self,
        force,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.force = force


class ForceProjections(Projections):
    """Force projections class."""

    __slots__ = ["force"]

    def __init__(
        self,
        force,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.force = force


class ForceMultiModelSelection(MultiModelSelection):
    """Base class for MultiModelSelection."""

    __slots__ = ["coefficients", "combinations", "hessian", "criterions", "weights"]

    def __init__(
        self,
        coefficients=None,
        combinations=None,
        hessian=None,
        criterions=None,
        weights=None,
    ) -> None:
        super().__init__()

        self.coefficients = coefficients
        self.combinations = combinations
        self.hessian = hessian
        self.criterions = criterions
        self.weights = weights
        return


class ForceInferrer(Inferrer):
    __slots__ = [
        "projections",
        "diffusion_estimator",
        "estimated_covariance",
        "nbpoints",
        "hessian",
    ]

    _coefficient_type = ForceCoefficients
    _projection_type = ForceProjections

    def __init__(
        self,
        projector: Projector | ProjectorGMGS,
        *args,
        projections: Optional[_projection_type] = None,
        coefficients: Optional[_coefficient_type] = None,
        orthonormalization_matrix: Optional[DataGroup] = None,
        diffusion_estimator: Optional[Callable] = None,
        estimated_covariance: Optional[DataGroup] = None,
        nbpoints: Optional[DataGroup] = None,
        hessian: Optional[DataGroup] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            projector,
            coefficients,  # type:ignore
            orthonormalization_matrix,
            *args,
            **kwargs,
        )
        self.diffusion_estimator = diffusion_estimator
        self.estimated_covariance = estimated_covariance
        self.nbpoints = nbpoints
        self.projections = projections
        self.hessian = hessian

    def __call__(
        self,
        data: Data,
        parameters: ParameterGroup,
        options: InferenceOptions = InferenceOptions(),
    ) -> None:
        (
            projections,
            orthonormalization_matrix,
            estimated_covariance,
            nbpoints,
        ) = self.projector.trajectory_integral.sum(
            self._project_on_basis,
            data,
            parameters=parameters,
            options=options,
        )

        self.projections = self.convert_projections(projections)
        self.orthonormalization_matrix = self.convert_orthonormalization_matrix(
            orthonormalization_matrix
        )
        self.estimated_covariance = estimated_covariance
        self.nbpoints = nbpoints
        return

    @partial(jax.jit, static_argnums=(0,))
    def _project_on_basis(
        self,
        data: Data,
        parameters: ParameterGroup,
        options: InferenceOptions = InferenceOptions(),
    ):
        """
        Projects on the non-orthonormalized basis.

        """

        # Basis
        if isinstance(self.projector, ProjectorGMGS):
            basis, orthogonalized_basis = self.projector(data, parameters)
            basis_array = basis.array
            orthogonalized_basis_array = orthogonalized_basis.array

            # The real basis i.e what the real force should look like
            basis_real = basis_array

            # The basis modified for the inference
            basis_inference = orthogonalized_basis_array
        else:
            basis = self.projector(data, parameters)
            basis_array = basis.array

            # The real basis i.e what the real force should look like
            basis_real = basis_array
            basis_inference = basis_array

        _, nbparticles, dof = basis_array.shape

        diffusion_array = self.diffusion_estimator(data, parameters["diffusion"])

        orthonormalization_matrix = self.projector.compute_basis_outer_product(
            basis_inference,
            diffusion_array * data.timestep,
        )

        force_projections = self._compute_motion_projections(
            data,
            basis_inference,
        )

        estimated_covariance = self._compute_estimated_covariance(
            data,
            basis_inference,
            basis_real,
            diffusion_array,
        )

        nbpoints = jnp.full(nbparticles, dof)

        return (
            force_projections,
            orthonormalization_matrix,
            estimated_covariance,
            nbpoints,
        )

    @partial(jax.jit, static_argnums=(0,))
    def _compute_motion_projections(
        self,
        data: Data,
        basis_values: jax.Array,
    ):
        # The ellipsis means to take the element-wise product over the remaining axes
        # and summing over them
        motion_projections = _einsum(
            "i...,ai...->ia",
            self.projector.projection_modifier(data.future_motions),
            basis_values,
        )

        return motion_projections

    @partial(jax.jit, static_argnums=(0,))
    def _compute_estimated_covariance(
        self,
        data: Data,
        basis_inference: jax.Array,
        basis_values: jax.Array,
        diffusion: jax.Array,
    ):
        motions = self.projector.projection_modifier(data.future_motions)

        r_1 = _einsum(
            "ai...m,im,jn,bj...n->iab",
            basis_inference,
            motions,
            motions,
            basis_inference,
        )

        r_2 = data.timestep * _einsum(
            "ai...m,im,ck...o,jkno,bj...n->iabc",
            basis_inference,
            motions,
            basis_values,
            diffusion,
            basis_inference,
        )

        r_3 = data.timestep * _einsum(
            "ai...m,ijmn,cj...n,ko,bk...o->iabc",
            basis_inference,
            diffusion,
            basis_values,
            motions,
            basis_inference,
        )

        r_4 = data.timestep**2 * _einsum(
            "ai...m,ijmn,cj...n,dk...o,klop,bl...p->iabcd",
            basis_inference,
            diffusion,
            basis_values,
            basis_values,
            diffusion,
            basis_inference,
        )

        return (r_1, r_2, r_3, r_4)

    @partial(jax.jit, static_argnums=(0,))
    def _optimize(
        self,
        combination,
        matrix,
        projections,
        estimated_covariance,
        nbpoints,
    ):
        select = jnp.outer(combination, combination)

        selected_matrix = _einsum("ab,...ab->...ab", select, matrix)
        inv_selected_matrix = jnp.linalg.pinv(selected_matrix)
        inv_hessian = 2 * inv_selected_matrix

        orthonormalized_coefficients = _einsum(
            "...ab,...b->...a",
            inv_selected_matrix,
            projections,
        )

        sigma = (
            _einsum(
                "...ab,a,b->...ab",
                estimated_covariance[0],
                combination,
                combination,
            )
            - _einsum(
                "...abc,a,b,...c->...ab",
                estimated_covariance[1],
                combination,
                combination,
                orthonormalized_coefficients,
            )
            - _einsum(
                "...abc,a,b,...c->...ab",
                estimated_covariance[2],
                combination,
                combination,
                orthonormalized_coefficients,
            )
            + _einsum(
                "...abcd,a,b,...c,...d->...ab",
                estimated_covariance[3],
                combination,
                combination,
                orthonormalized_coefficients,
                orthonormalized_coefficients,
            )
        )

        inv_sigma_m = inv_hessian

        Hn_trace = _einsum("...ab,...bc->...ac", inv_sigma_m, sigma)
        Hn_det = Hn_trace + jnp.where(
            jnp.diag(jnp.logical_not(combination)),
            1.0,
            0.0,
        )

        nllh = -0.5 * _einsum(
            "...a,...a->...",
            projections * combination,
            orthonormalized_coefficients,
        ) + 0.25 * _einsum(
            "...a,...b,...ab",
            orthonormalized_coefficients,
            orthonormalized_coefficients,
            selected_matrix,
        )

        b_m = jnp.sum(combination)
        b_max = combination.shape[0]
        logdetH = jnp.log(jnp.linalg.det(Hn_det))
        trH = _einsum("...aa->...", Hn_trace)

        # Akaike based criterions (Kullback-Leibler divergence)
        aic = 2 * nllh + 2 * b_m
        aicc = aic + jnp.true_divide(b_m * (b_m + 1), nbpoints - b_m - 1)
        gic = 2 * nllh + jnp.log(nbpoints) + jnp.log(jnp.log(b_max)) * b_m
        gaic = 2 * nllh + 2 * trH

        # Bayesian based criterions
        bic = 2 * nllh + jnp.log(nbpoints) * b_m
        gbic = bic - logdetH
        gbicp = gbic + trH
        ebic = bic + jnp.log(binomial_coefficient(b_max, b_m))
        hgbicp = (
            2 * nllh + 2 * jnp.log(b_max * jnp.sqrt(nbpoints)) * b_m + trH - logdetH
        )

        criterions = jnp.stack(
            [
                nllh,
                bic,
                gbic,
                gbicp,
                aic,
                gaic,
                ebic,
                gic,
                hgbicp,
                aicc,
            ],
            axis=-1,
        )

        return criterions

    def optimize(
        self,
        matrix: Optional[DataGroup] = None,
        projections: Optional[DataGroup] = None,
        estimated_covariance: Optional[Tuple[DataGroup]] = None,
        nbpoints: Optional[DataGroup] = None,
    ):
        combinations, _ = create_member_set(jnp.asarray([0, 1]), self.projections.force.shape[-1])  # type: ignore

        matrix = self.orthonormalization_matrix.array if matrix is None else matrix.array  # type: ignore

        projections = self.projections.force.array if projections is None else projections.array  # type: ignore

        estimated_covariance = jax.tree_util.tree_map(
            lambda x: x.array,
            (
                self.estimated_covariance
                if estimated_covariance is None
                else estimated_covariance
            ),
            is_leaf=lambda node: isinstance(node, DataGroup),
        )

        nbpoints = self.nbpoints.array if nbpoints is None else nbpoints.array  # type: ignore

        criterions = shs.shard_function(
            self._optimize,
            mesh=shs.create_mesh("combination"),
            axis_name="combination",
        )(
            combinations,
            matrix=matrix,
            projections=projections,  # type: ignore
            estimated_covariance=estimated_covariance,
            nbpoints=nbpoints,  # type: ignore
        )

        best_combinations = self._get_best_model(criterions, combinations)

        hessian, coefficients = self._compute_hessian_coefficients(
            best_combinations,
            matrix,
            projections,
        )

        return ForceMultiModelSelection(
            coefficients=self.convert_coefficients(coefficients),
            combinations=self.convert_coefficients(best_combinations),
            hessian=self.convert_hessian(hessian),
        )

    @partial(jax.jit, static_argnums=(0,), static_argnames=("keep",))
    def _sort_optimization(self, criterions, coefficients, keep=1000):

        def compute_weights(criterions):

            best = jnp.nanmin(criterions, axis=-1)

            distance = criterions - best[..., jnp.newaxis]

            weights = jnp.exp(-0.5 * distance)
            weight_sum = jnp.nansum(weights, axis=-1)
            weights = jnp.true_divide(weights, weight_sum[..., jnp.newaxis])
            return weights

        # Anormal cirterion values set to infinity
        criterions = jnp.nan_to_num(
            criterions,
            nan=jnp.inf,
            posinf=jnp.inf,
            neginf=jnp.inf,
        )

        # Reshape criterions and coefficients such that the 1st axis correspond
        # to the different groups and/or criterions
        reshaped_criterions = _einsum("a...->...a", criterions)
        reshaped_coefficients = _einsum("a...b->...ab", coefficients)

        weights = compute_weights(reshaped_criterions)
        weights_shape = weights.shape

        flat_weights = weights.reshape(-1, weights_shape[-1])
        flat_criterions = reshaped_criterions.reshape(-1, weights_shape[-1])

        coefficient_shape = reshaped_coefficients.shape
        flat_coefficients = reshaped_coefficients.reshape(-1, *coefficient_shape[-2:])

        # def func(weights, criterions):
        #     order = jnp.argsort(weights, descending=True)[:keep]
        #     return (order, weights[order], criterions[order])

        def scan_func(_, args):
            weights, criterions = args
            order = jnp.argsort(weights, descending=True)[:keep]
            return (None, (order, weights[order], criterions[order]))

        _order, _ordered_weights, _ordered_criterions = jax.lax.scan(
            scan_func,
            None,
            (flat_weights, flat_criterions),
        )[-1]
        # jax.vmap(func)(
        #     flat_weights,
        #     flat_criterions,
        # )

        # Get the ordering based on criterions
        order, ordered_weights, ordered_criterions = jax.tree_util.tree_map(
            lambda array: array.reshape(*weights_shape[:-1], keep),
            (_order, _ordered_weights, _ordered_criterions),
        )

        # Reorder the coefficients based on the previous ordering
        best_coefficients = jax.vmap(
            jax.vmap(
                lambda order, coeff: coeff[order[0]],
                in_axes=(0, None),
            ),
            in_axes=(0, 0),
        )(
            order.reshape(-1, *order.shape[-2:]),
            flat_coefficients,
        ).reshape(
            *order.shape[:-1], coefficients.shape[-1]
        )

        return order, ordered_criterions, ordered_weights, best_coefficients

    @partial(jax.jit, static_argnums=(0,))
    def _get_best_model(self, criterions, combinations):

        # Anormal cirterion values set to infinity
        criterions = jnp.nan_to_num(
            criterions,
            nan=jnp.inf,
            posinf=jnp.inf,
            neginf=jnp.inf,
        )

        best_indices = jnp.nanargmin(
            _einsum("a...->...a", criterions), axis=-1
        ).flatten()

        _best_combinations = jax.lax.scan(
            lambda _, index: (None, combinations[index]), None, best_indices
        )[-1]

        best_combinations = _best_combinations.reshape(
            *criterions.shape[1:], combinations.shape[-1]
        )

        return best_combinations

    @partial(jax.jit, static_argnums=(0))
    def _compute_hessian_coefficients(self, combinations, matrices, projections):

        masks = _einsum("...ca,...cb->...cab", combinations, combinations)

        selected_matrix = _einsum("...cab,...ab->...cab", masks, matrices)
        inv_selected_matrix = jnp.linalg.pinv(selected_matrix)

        orthonormalized_coefficients = _einsum(
            "...cab,...cb->...ca",
            inv_selected_matrix,
            # Mask the projections
            _einsum("...ca,...a->...ca", combinations, projections),
        )

        return -0.5 * selected_matrix, orthonormalized_coefficients


# class ForceInferrer(Inferrer):
#     __slots__ = [
#         "projections",
#         "diffusion_estimator",
#         "true_covariance",
#         "nbpoints",
#         "hessian",
#     ]
#
#     _coefficient_type = ForceCoefficients
#     _projection_type = ForceProjections
#
#     def __init__(
#         self,
#         projector: Projector,
#         *args,
#         projections: Optional[_projection_type] = None,
#         coefficients: Optional[_coefficient_type] = None,
#         orthonormalization_matrix: Optional[DataGroup] = None,
#         diffusion_estimator: Optional[Callable] = None,
#         true_covariance: Optional[DataGroup] = None,
#         nbpoints: Optional[DataGroup] = None,
#         hessian: Optional[DataGroup] = None,
#         **kwargs,
#     ) -> None:
#         super().__init__(
#             projector,
#             coefficients,
#             orthonormalization_matrix,
#             *args,
#             **kwargs,
#         )
#         self.diffusion_estimator = diffusion_estimator
#         self.true_covariance = true_covariance
#         self.nbpoints = nbpoints
#         self.projections = projections
#         self.hessian = hessian
#
#     def __call__(
#         self,
#         data: Data,
#         parameters: ParameterGroup,
#         options: InferenceOptions = InferenceOptions(),
#     ) -> None:
#         (
#             projections,
#             orthonormalization_matrix,
#             nbpoints,
#             true_covariance,
#         ) = self.projector.trajectory_integral.sum_func(
#             self._project_on_basis,
#             data,
#             parameters=parameters,
#             options=options,
#             message="",
#             # message="Projecting motions on the basis",
#         )
#
#         self.projections = self.convert_projections(projections)
#
#         _orthonormalization_matrix_type = OrthonormalizationMatrix(
#             interactions=self.projector.basis.function.functions
#         )
#
#         self.orthonormalization_matrix = orthonormalization_matrix.map(
#             lambda matrix: _orthonormalization_matrix_type.regroup(matrix),
#         )
#
#         self.true_covariance = true_covariance
#         self.nbpoints = nbpoints
#         return
#
#     @partial(jax.jit, static_argnums=(0,))
#     def _compute_motion_projections(
#         self,
#         data: Data,
#         basis_values: jax.Array,
#     ):
#         # The ellipsis means to take the element-wise product over the remaining axes
#         # and summing over them
#         motion_projections = _einsum(
#             "i...,ai...->ia",
#             self.projector.projection_modifier(data.future_motions),
#             basis_values,
#         )
#
#         return motion_projections
#
#     @partial(jax.jit, static_argnums=(0,))
#     def _compute_true_covariance(
#         self,
#         data: Data,
#         basis_values: jax.Array,
#         diffusion: jax.Array,
#     ):
#         motions = self.projector.projection_modifier(data.future_motions)
#
#         r_1 = _einsum(
#             "ai...m,im,jn,bj...n->iab",
#             basis_values,
#             motions,
#             motions,
#             basis_values,
#         )
#
#         r_2 = data.timestep * _einsum(
#             "ai...m,im,ck...o,jkno,bj...n->iabc",
#             basis_values,
#             motions,
#             basis_values,
#             diffusion,
#             basis_values,
#         )
#
#         r_3 = data.timestep * _einsum(
#             "ai...m,ijmn,cj...n,ko,bk...o->iabc",
#             basis_values,
#             diffusion,
#             basis_values,
#             motions,
#             basis_values,
#         )
#
#         r_4 = data.timestep**2 * _einsum(
#             "ai...m,ijmn,cj...n,dl...p,klop,bk...o->iabcd",
#             basis_values,
#             diffusion,
#             basis_values,
#             basis_values,
#             diffusion,
#             basis_values,
#         )
#
#         return (r_1, r_2, r_3, r_4)
#
#     def optimize(self):
#         # Get the number of parameters per group
#         # nbparameters = tuple(param[0] for param in parameters.shape[1])
#         nbparameters = tuple(p.shape[0] for p in self.projections.force[0][0])
#         _combinations = self._optimize(nbparameters)
#
#         self.coefficients = self.projector.trajectory_integral.map(
#             lambda _, comb, proj, mat: type(self)._coefficient_type(
#                 BasisCriterions(
#                     [
#                         self._compute_coefficients(nbparameters, c, proj, mat)
#                         for c in comb.array
#                     ]
#                 )
#             ),
#             _combinations,
#             self.projections.force,
#             self.orthonormalization_matrix,
#         )
#
#         self.hessian = self.projector.trajectory_integral.map(
#             lambda _, comb, mat: BasisCriterions(
#                 [self._compute_hessian(nbparameters, c, mat) for c in comb.array]
#             ),
#             _combinations,
#             self.orthonormalization_matrix,
#         )
#
#         return
#
#     @partial(jax.jit, static_argnums=(0, 1))
#     def _optimize(self, nbparameters):
#         total_nbparameters = sum(nbparameters)
#         combinations, _ = create_member_set(
#             jnp.asarray([0, 1]),
#             total_nbparameters,
#         )
#
#         # @ProgressBarScan(nbcombinations, message="Computing Criterions")
#         def _compute_criterions_combinations(carry, xs):
#             projections, matrix, nbp, true_covariance = carry
#             combination = xs
#             return (
#                 carry,
#                 self._test_bases(
#                     nbparameters,
#                     combination,
#                     nbp,
#                     matrix,
#                     projections,
#                     *true_covariance,
#                 ),
#             )
#
#         _carry = (
#             self.projections.force,
#             self.orthonormalization_matrix,
#             self.nbpoints,
#             self.true_covariance,
#         )
#
#         best_combinations = self.projector.trajectory_integral.map(
#             lambda _, arr: BasisCriterions(combinations[arr]),
#             jnp.nanargmin(
#                 jax.lax.scan(
#                     _compute_criterions_combinations,
#                     _carry,
#                     combinations,
#                 )[-1],
#                 axis=0,
#             ),
#         )
#
#         return best_combinations
#
#     @partial(jax.jit, static_argnums=(0, 1))
#     def _test_bases(
#         self,
#         nbparameters,
#         combination,
#         nbpoints,
#         matrix,
#         projections,
#         *true_covariance,
#     ):
#         select = jnp.outer(combination, combination)
#
#         def _compute_criterions(
#             matrix, projections, nbpoints, *true_covariance, select=None
#         ):
#             selected_matrix = select * matrix
#             inv_selected_matrix = jnp.zeros_like(matrix)
#
#             _offset = 0
#             for i in nbparameters:
#                 _end = _offset + i
#                 inv_selected_matrix = inv_selected_matrix.at[
#                     _offset:_end, _offset:_end
#                 ].set(jnp.linalg.pinv(selected_matrix[_offset:_end, _offset:_end]))
#
#                 _offset += i
#             inv_hessian = 2 * inv_selected_matrix
#
#             orthonormalized_coefficients = jnp.matmul(inv_selected_matrix, projections)
#
#             sigma = (
#                 _einsum(
#                     "ab,a,b->ab",
#                     true_covariance[0],
#                     combination,
#                     combination,
#                 )
#                 # plus to minux
#                 - _einsum(
#                     "abc,a,b,c->ab",
#                     true_covariance[1],
#                     combination,
#                     combination,
#                     orthonormalized_coefficients,
#                 )
#                 # plus to minus
#                 - _einsum(
#                     "abc,a,b,c->ab",
#                     true_covariance[2],
#                     combination,
#                     combination,
#                     orthonormalized_coefficients,
#                 )
#                 + _einsum(
#                     "abcd,a,b,c,d->ab",
#                     true_covariance[3],
#                     combination,
#                     combination,
#                     orthonormalized_coefficients,
#                     orthonormalized_coefficients,
#                 )
#             )
#
#             inv_sigma_m = inv_hessian
#
#             Hn_trace = inv_sigma_m @ sigma
#             Hn_det = inv_sigma_m @ sigma + jnp.where(
#                 jnp.diag(jnp.logical_not(combination)),
#                 1.0,
#                 0.0,
#             )
#
#             nllh = -0.5 * _einsum(
#                 "a,a",
#                 projections * combination,
#                 orthonormalized_coefficients,
#             ) + 0.25 * _einsum(
#                 "a,b,ab",
#                 orthonormalized_coefficients,
#                 orthonormalized_coefficients,
#                 selected_matrix,
#             )
#
#             b_m = jnp.sum(combination)
#             b_max = combination.shape[0]
#             aic = 2 * nllh + 2 * b_m
#             bic = 2 * nllh + jnp.log(nbpoints) * b_m
#
#             logdetH = jnp.log(jnp.linalg.det(Hn_det))
#             trH = jnp.trace(Hn_trace)
#
#             gbic = bic - logdetH
#             gbicp = gbic + trH
#             gaic = 2 * nllh + 2 * trH
#             ebic = bic + jnp.log(binomial_coefficient(b_max, b_m))
#             gic = 2 * nllh + jnp.log(nbpoints) + jnp.log(jnp.log(b_max)) * b_m
#             hgbicp = (
#                 2 * nllh + 2 * jnp.log(b_max * jnp.sqrt(nbpoints)) * b_m + trH - logdetH
#             )
#
#             return jnp.asarray(
#                 [
#                     nllh,
#                     bic,
#                     gbic,
#                     gbicp,
#                     aic,
#                     gaic,
#                     ebic,
#                     gic,
#                     hgbicp,
#                 ]
#             )
#
#         return matrix.vmap(
#             _compute_criterions,
#             2,
#             projections,
#             nbpoints,
#             *true_covariance,
#             select=select,
#         )
#
#     @partial(jax.jit, static_argnums=(0, 1))
#     def _compute_coefficients(self, nbparameters, combination, projection, mat):
#         coefficients = jnp.zeros_like(projection.array)
#
#         _select = jnp.outer(combination, combination)
#         _start = 0
#
#         for nb in nbparameters:
#             _end = _start + nb
#             _mask = _select[_start:_end, _start:_end]
#             inv_matrix = jnp.linalg.pinv(_mask * mat.array[_start:_end, _start:_end])
#             coefficients = coefficients.at[_start:_end].set(
#                 jnp.matmul(inv_matrix, projection.array[_start:_end])
#             )
#             _start += _end
#
#         return projection.regroup(coefficients)
#
#     @partial(jax.jit, static_argnums=(0, 1))
#     def _compute_hessian(self, nbparameters, combination, mat):
#         hessian = jnp.zeros_like(mat.array)
#
#         _select = jnp.outer(combination, combination)
#         _start = 0
#
#         for nb in nbparameters:
#             _end = _start + nb
#             _mask = _select[_start:_end, _start:_end]
#             _matrix = _mask * mat.array[_start:_end, _start:_end]
#             hessian = hessian.at[_start:_end, _start:_end].set(_matrix)
#             _start += _end
#
#         return -0.5 * hessian
#
#
# class ForceItoInferrer(ForceInferrer):
#     """Inferrer using Ito integration."""
#
#     __slots__ = []
#
#     @partial(jax.jit, static_argnums=(0,))
#     def _project_on_basis(
#         self,
#         data: Data,
#         parameters: ParameterGroup,
#         options: InferenceOptions = InferenceOptions(),
#     ):
#         """
#         Projects on the non-orthonormalized basis.
#
#         """
#
#         basis_values = self.projector(data, parameters).array
#         _, nbparticles, dof = basis_values.shape
#
#         if callable(self.diffusion_estimator):
#             diffusion_parameters = parameters["diffusion"]
#             _diffusion = self.diffusion_estimator(data, diffusion_parameters).array[0]
#
#         elif isinstance(self.diffusion_estimator, jax.Array):
#             _diffusion = split_matrix(self.diffusion_estimator, dof, dof)
#         else:
#             _diffusion = split_matrix(jnp.eye(nbparticles * dof), dof, dof)
#
#         orthonormalization_matrix = self.projector.compute_basis_outer_product(
#             basis_values,
#             _diffusion * data.timestep,
#         )
#
#         force_projections = self._compute_motion_projections(
#             data,
#             basis_values,
#         )
#
#         true_covariance = self._compute_true_covariance(
#             data,
#             basis_values,
#             _diffusion,
#         )
#
#         nbpoints = jnp.full(nbparticles, dof)
#
#         return (
#             force_projections,
#             orthonormalization_matrix,
#             nbpoints,
#             true_covariance,
#         )
