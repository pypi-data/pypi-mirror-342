__all__ = [
    "DriftAnsatz",
    "DriftCoefficients",
    "DriftError",
    "DriftInformation",
    "DriftStratonovitchInferrer",
    "DriftItoInferrer",
    "DriftItoInferrerNL",
]

from abc import abstractmethod
from collections import namedtuple
from collections.abc import Callable
from functools import partial
from math import prod
from types import NoneType
from typing import Dict

import jax
import jax.numpy as jnp
import jax.scipy as jsp
from jax import lax
from jax.scipy.optimize import minimize

from sfx.basis.basis import Basis
from sfx.basis.interactions import Interactions
from sfx.basis.parameters import ParameterGroup, Parameters
from sfx.core.sfx_object import SFXCallable, SFXIterable
from sfx.helpers.math import (group_iterative_mgs, recombine_matrix,
                              split_matrix)
from sfx.inference.data import Data
from sfx.inference.estimators.diffusion import DiffusionEstimator
from sfx.inference.inferrer.core import (Ansatz, Coefficients,
                                         InferenceOptions, Inferrer,
                                         InferrerNL)
from sfx.inference.inferrer.diffusion import DiffusionAnsatz
from sfx.inference.projector import Projector, TrajectoryIntegral
from sfx.inference.statistics import Statistics

# from jaxlib.xla_extension import DeviceArray


class DriftAnsatz(Ansatz):
    """Drift ansatz."""

    __slots__ = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class DriftCoefficients(Coefficients):
    """Drift coefficients class."""

    __slots__ = ["drift", "velocity", "diffusive_current"]

    TypeCoefficients = jax.Array | None

    def __init__(
        self,
        drift,
        velocity: TypeCoefficients = None,
        diffusive_current: TypeCoefficients = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.drift = drift
        self.velocity = velocity
        self.diffusive_current = diffusive_current


class DriftInformation(SFXCallable):
    __slots__ = [
        "drift_ansatz",
        "diffusion_estimator",
        "trajectory_integral",
        "partial",
    ]

    def __init__(self, statistics=Statistics(), *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.partial = statistics

    def __call__(
        self,
        data: Data,
        drift_ansatz: DriftAnsatz,
        diffusion_estimator: DiffusionEstimator,
        trajectory_integral: TrajectoryIntegral,
    ):
        super().__call__()

        self.drift_ansatz = drift_ansatz
        self.diffusion_estimator = diffusion_estimator
        self.trajectory_integral = trajectory_integral

        mean = self._compute_information(data)

        self.partial = Statistics(
            mean=mean,
            bias=jnp.full_like(mean, 0.25 / mean.shape[-1]),
            error=jnp.sqrt(2 * mean + 0.25),
        )

    @partial(jax.jit, static_argnums=(0,))
    def _compute_information(self, data: Data):
        """Computes the information about the drift."""

        def compute_capacity(data):
            inverse_diffusion = split_matrix(
                jnp.real(
                    jnp.linalg.pinv(recombine_matrix(self.diffusion_estimator(data)))
                ),
                data.coordinates.dof,
                data.coordinates.dof,
            )
            drift = self.drift_ansatz(data.coordinates, data.time)

            return 0.25 * jnp.einsum(
                "ima,ijmn,jna->iamn",
                drift,
                inverse_diffusion,
                drift,
                precision=lax.Precision.HIGHEST,
            )

        return self.trajectory_integral.integrate(
            compute_capacity, data, "Computing information"
        )

    @property
    def total(self):
        mean = jnp.sum(self.partial.mean)
        nb_basis_functions = self.partial.mean.shape[2]

        return Statistics(
            mean=mean,
            bias=0.5 * nb_basis_functions,
            error=jnp.sqrt(2 * mean + 0.25 * nb_basis_functions**2),
        )

    @property
    def cumulative(self):
        dof = self.partial.mean.shape[-1]
        mean = jnp.nancumsum(jnp.nansum(self.partial.mean, axis=(-2, -1)))

        return Statistics(
            mean=mean,
            bias=0.25 * dof * jnp.arange(1, len(mean) + 1),
            error=jax.vmap(
                lambda info, n: jnp.sqrt(2 * info + 0.25 * (dof * n) ** 2),
                in_axes=(0, 0),
                out_axes=0,
            )(
                mean,
                jnp.arange(1, len(mean) + 1),
            ),
        )


class DriftError(SFXCallable):
    __slots__ = [
        "information",
        "trajectory_length",
        "discretization",
    ]

    def __init__(
        self,
        information: DriftInformation,
        trajectory_length: float = jnp.nan,
        discretization: float = jnp.nan,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.information = information
        self.trajectory_length = trajectory_length
        self.discretization = discretization

    def __call__(self, data: Data):
        super().__call__()

        if not self.information:
            self.information(
                data,
                drift_ansatz=self.information.drift_ansatz,
                diffusion_estimator=self.information.diffusion_estimator,
                trajectory_integral=self.information.trajectory_integral,
            )

        self.trajectory_length = (
            0.5 * self.information.partial.mean.shape[2] / self.information.total.mean
        )

        self.discretization = self._compute_discretization_error(data)

    @partial(jax.jit, static_argnums=(0,))
    def _compute_discretization_error(self, data: Data):
        """Computes the information about the drift."""

        @jax.jit
        def compute_main_term(data):
            ansatz_grad_ansatz = jnp.einsum(
                "ima,imajn->ijn",
                self.information.drift_ansatz(data.coordinates, data.time),
                self.information.drift_ansatz.gradient(
                    data.coordinates, data.time
                )._combine(),
            )

            inverse_diffusion = split_matrix(
                jnp.real(
                    jnp.linalg.pinv(
                        recombine_matrix(self.information.diffusion_estimator(data))
                    )
                ),
                data.coordinates.dof,
                data.coordinates.dof,
            )

            return (
                jnp.einsum(
                    "ijm,ijmn,ijn->i",
                    ansatz_grad_ansatz,
                    inverse_diffusion,
                    ansatz_grad_ansatz,
                )
                * data.timestep**2
            )

        return (
            0.25
            * self.information.trajectory_integral.average(
                compute_main_term, data, "Computing Discretization Error"
            )
        ) / (self.information.total.mean / data.trajectory_length)

    @property
    def total(self):
        return self.trajectory_length + self.discretization


class DriftInferrer(Inferrer):
    __slots__ = ["diffusion_estimator"]

    _coefficient_type = DriftCoefficients

    def __init__(
        self,
        projector: Projector,
        coefficients: DriftCoefficients | None = None,
        orthonormalization_matrix: jax.Array | None = None,
        diffusion_estimator: jax.Array | Callable | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            projector, coefficients, orthonormalization_matrix, *args, **kwargs
        )
        self.diffusion_estimator = diffusion_estimator

    @partial(jax.jit, static_argnums=(0,))
    def _compute_velocity_projections(
        self,
        data: Data,
        basis_values: jax.Array,
        transform_values: jax.Array | None,
    ):
        # The ellipsis means to take the element-wise product over the remaining axes
        # and summing over them
        if transform_values is not None:
            velocity_projections = jnp.einsum(
                "j...n,ijmn,ai...m->ia",
                self.projector.projection_modifier(data.velocities),
                transform_values,
                basis_values,
                precision=lax.Precision.HIGHEST,
            )
        else:
            velocity_projections = jnp.einsum(
                "i...,ai...->ia",
                self.projector.projection_modifier(data.velocities),
                basis_values,
                precision=lax.Precision.HIGHEST,
            )

        return velocity_projections

    @partial(jax.jit, static_argnums=(0,))
    def _compute_basis_svd(self, basis_values):
        _B = jnp.moveaxis(basis_values, (0, 1, -1), (-1, 0, 1))
        basis_shape = _B.shape

        # Total degrees of freedom
        nu = prod(_B.shape[:2])

        # Transforms the basis into a matrix
        B = _B.reshape(nu, -1)
        b = B.shape[-1]

        # Computes the SVD and select only singular values above a threshold
        U, _S, Vh = jsp.linalg.svd(B)
        _mask = _S > _S.max() * jnp.where(nu > b, nu, b) * jnp.finfo(1.0).eps
        S = jnp.zeros_like(B).at[jnp.diag_indices(b, 2)].set(_mask * _S)

        return jnp.moveaxis(
            (U @ S @ Vh).reshape(*basis_shape),
            (-1, 0, 1),
            (0, 1, -1),
        )

    @partial(jax.jit, static_argnums=(0,))
    def _compute_gmgs(self, basis):
        return group_iterative_mgs(basis)

    @partial(jax.jit, static_argnums=(0,))
    def _compute_bridge(self, basis, data, parameters, length):
        def _interpolator(i, val):
            data, parameters, output = val
            _delta_coord = (
                data.coordinates + i * jnp.reciprocal(length) * data.future_motions
            )
            _delta_time = data.time + i * jnp.reciprocal(length) * data.timestep
            delta_data = type(data)(
                time=_delta_time,
                timestep=data.timestep,
                coordinates=_delta_coord,
                future_motions=data.future_motions,
                past_motions=data.past_motions,
                coordinates_stratonovitch=data.coordinates_stratonovitch,
                velocities=data.velocities,
                nbparticles=data.nbparticles,
            )
            _incr = self.projector.basis(delta_data, parameters).array
            return (data, parameters, output + _incr)

        result = jax.lax.fori_loop(
            1,
            length,
            _interpolator,
            (data, parameters, basis.array),
        )

        return basis.regroup(result[-1])


class DriftItoInferrer(DriftInferrer):
    """Inferrer using Ito integration."""

    __slots__ = []

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

        if callable(self.diffusion_estimator):
            basis_parameters = parameters[0]
            diffusion_parameters = parameters[1]
            basis = self.projector.basis(data, basis_parameters)
            basis = jax.lax.cond(
                options.use_bridge,
                self._compute_bridge,
                lambda basis, *_: basis,
                basis,
                data,
                basis_parameters,
                options.use_bridge,
            )
            basis_values = jax.lax.cond(
                options.use_gmgs,
                self._compute_gmgs,
                lambda bv: bv,
                basis,
            ).array

            inverse_diffusion = split_matrix(
                jnp.linalg.pinv(
                    recombine_matrix(
                        self.diffusion_estimator(data, diffusion_parameters).array[0]
                    )
                ),
                basis_values.shape[-1],
                basis_values.shape[-1],
            )

        elif isinstance(self.diffusion_estimator, jax.Array):
            basis = self.projector.basis(data, parameters)
            basis = jax.lax.cond(
                options.use_bridge,
                self._compute_bridge,
                lambda basis, *_: basis,
                basis,
                data,
                parameters,
                options.use_bridge,
            )

            basis_values = jax.lax.cond(
                options.use_gmgs,
                self._compute_gmgs,
                lambda bv: bv,
                basis,
            ).array

            inverse_diffusion = split_matrix(
                jnp.linalg.pinv(self.diffusion_estimator),
                basis_values.shape[-1],
                basis_values.shape[-1],
            )

        else:
            inverse_diffusion = self.diffusion_estimator
            basis = self.projector.basis(data, parameters)
            basis_values = jax.lax.cond(
                options.use_gmgs,
                self._compute_gmgs,
                lambda bv: bv,
                basis,
            ).array

        basis_values = jax.lax.cond(
            options.use_svd,
            self._compute_basis_svd,
            lambda bv: bv,
            basis_values,
        )

        orthonormalization_matrix = self.projector._compute_basis_outer_product(
            None,
            basis_values,
            None,
        )

        # information_matrix = self.projector._compute_basis_outer_product(
        #     None,
        #     basis_values,
        #     inverse_diffusion,
        # )

        drift_coefficients = self._compute_velocity_projections(
            data,
            basis_values,
            inverse_diffusion,
        )

        return (
            drift_coefficients,
            orthonormalization_matrix,
            # information_matrix,
        )


class DriftStratonovitchInferrer(DriftInferrer):
    __slots__ = ["diffusion_estimator"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __call__(
        self,
        data: Data,
        interactions: Interactions,
        parameters: Parameters,
        trajectory_integral: TrajectoryIntegral,
        diffusion_estimator: DiffusionEstimator,
        projection_modifier: Callable | None = None,
    ) -> None:
        super().__call__()

        basis = Basis(interactions, parameters)
        self.projector = Projector(basis, trajectory_integral, projection_modifier)
        self.diffusion_estimator = diffusion_estimator

        (
            velocity_projections,
            velocity_coefficients,
            diffusive_current_projections,
            diffusive_current_coefficients,
            drift_projections,
            drift_coefficients,
        ) = self._project_on_basis(data)

        self.projections = DriftProjections(
            drift_projections,
            velocity_projections,
            diffusive_current_projections,
        )

        self.coefficients = DriftCoefficients(
            drift_coefficients,
            velocity_coefficients,
            diffusive_current_coefficients,
        )

    @partial(jax.jit, static_argnums=(0,))
    def _project_on_basis(self, data: Data):
        orthonormalization_matrix = self.projector(data)

        # Projecting the velocities (irreversible currents)
        velocity_projections = self.projector.orthonormalize(
            self.projector.trajectory_integral.average(
                self._compute_velocity_projections,
                data,
                "Projecting velocities onto the basis",
            ),
            orthonormalization_matrix.transpose(0, 1, 3, 2),
        )

        velocity_coefficients = self.projector.orthonormalize(
            velocity_projections,
            orthonormalization_matrix,
        )

        # Projecting the diffusive currents (reversible currents)
        diffusive_current_projections = self.projector.orthonormalize(
            self.projector.trajectory_integral.average(
                self._compute_diffusive_current_projections,
                data,
                "Projecting diffusive currents onto the basis",
            ),
            # Take the transpose on the two last axes
            orthonormalization_matrix.transpose(0, 1, 3, 2),
        )

        diffusive_current_coefficients = self.projector.orthonormalize(
            diffusive_current_projections,
            orthonormalization_matrix,
        )

        # Reconstructing the drift
        drift_projections = velocity_projections + diffusive_current_projections

        drift_coefficients = self.projector.orthonormalize(
            drift_projections,
            orthonormalization_matrix,
        )

        return (
            velocity_projections,
            velocity_coefficients,
            diffusive_current_projections,
            diffusive_current_coefficients,
            drift_projections,
            drift_coefficients,
        )

    @partial(jax.jit, static_argnums=(0,))
    def _compute_velocity_projections(self, data: Data):
        basis_values = self.projector.basis.function(
            data.coordinates_stratonovitch, data.time
        )

        # The indices "an" run over the basis function.
        velocity_projections = jnp.einsum(
            "im,ian->iman",
            self.projector.projection_modifier(data.velocities),
            basis_values,
            precision=lax.Precision.HIGHEST,
        ).reshape(data.coordinates.nbparticles, data.coordinates.dof, -1)

        return velocity_projections

    @partial(jax.jit, static_argnums=(0,))
    def _compute_diffusive_current_projections(self, data: Data):
        diffusive_current_projections = -jnp.einsum(
            "ijmn,iasjn->imas",
            # Add the mode in self.diffusion_estimator : coordinates or stratonovitch or else
            self.diffusion_estimator(data),
            # Gadient has shape (nbparticles, nbfunctions, dof, nbparticles, dof)
            self.projector.projection_modifier(
                self.projector.basis.gradient(
                    data[self.diffusion_estimator.evaluation_point], data.time
                )
            ),
            precision=lax.Precision.HIGHEST,
        ).reshape(
            data.coordinates.nbparticles,
            data.coordinates.dof,
            -1,
        )

        return diffusive_current_projections


class DriftInferrerNL(InferrerNL):
    __slots__ = []

    def __init__(
        self,
        projector: Projector,
        average_inverse_diffusion,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            projector,
            average_inverse_diffusion,
            *args,
            **kwargs,
        )

    @partial(jax.jit, static_argnums=(0, 1))
    def _minimize(
        self, cost_function: Callable, data: Data, parameters: ParameterGroup
    ):
        results = self.projector.trajectory_integral.dispatch_integrate(
            partial(minimize, method="BFGS"),
            cost_function,
            data,
            args=(parameters, data),
        )

        return results


class DriftItoInferrerNL(DriftInferrerNL):
    __slots__ = []

    @partial(jax.jit, static_argnums=(0,))
    def cost_function(self, parameters, data):
        Scannee = namedtuple("Scannee", "basis_values data")

        basis_values = self.projector.compute_basis(data, parameters)

        _, local_cost = jax.lax.scan(
            lambda _, x: (
                None,
                jnp.einsum(
                    "aim,ajn,ijmn->i",
                    x.basis_values,
                    x.basis_values
                    - 2 * self.projector.projection_modifier(x.data.velocities),
                    self.average_inverse_diffusion,
                    precision=jax.lax.Precision.HIGHEST,
                ),
            ),
            None,
            Scannee(basis_values, data),
        )

        return local_cost
