""""""

__all__ = [
    "DiffusionAnsatz",
    # "DiffusionProjections",
    "DiffusionCoefficients",
    "DiffusionInferrer",
    "DiffusionInferrerNL",
]

from abc import abstractmethod
from collections import namedtuple
from functools import partial
from typing import Optional

import jax
import jax.numpy as jnp
from jax import lax
from jax.tree_util import Partial
from jax.scipy.optimize import minimize

from sfx.basis.parameters import ParameterGroup, Parameters
from sfx.core.sfx_object import SFXObject
from sfx.inference.data import Data
from sfx.inference.estimators.diffusion import DiffusionEstimator
from sfx.inference.inferrer.core import (
    Ansatz,
    Coefficients,
    Inferrer,
    InferrerNL,
    Projections,
    InferenceOptions,
    MultiModelSelection,
)
from sfx.inference.projector import Projector, ProjectorGMGS

_einsum = Partial(jnp.einsum, precision=jax.lax.Precision.HIGHEST)


class DiffusionAnsatz(Ansatz):
    """Diffusion ansatz."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class DiffusionCoefficients(Coefficients):
    """Diffusion coefficients"""

    __slots__ = ["diffusion"]

    def __init__(self, diffusion, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.diffusion = diffusion


class DiffusionProjections(Projections):
    """Diffusion projections class."""

    __slots__ = ["diffusion"]

    def __init__(
        self,
        diffusion,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.diffusion = diffusion


class DiffusionMultiModelSelection(MultiModelSelection):
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


class DiffusionInferrer(Inferrer):
    __slots__ = ["diffusion_estimator", "projections"]

    _coefficient_type = DiffusionCoefficients
    _projection_type = DiffusionProjections

    def __init__(
        self,
        projector: Projector,
        diffusion_estimator: DiffusionEstimator,
        *args,
        projections: Optional[_projection_type] = None,
        coefficients: Optional[_coefficient_type] = None,
        orthonormalization_matrix: jax.Array | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            projector,
            coefficients,  # type:ignore
            orthonormalization_matrix,  # type:ignore
            *args,
            **kwargs,
        )
        self.diffusion_estimator = diffusion_estimator
        self.projections = projections

    def __call__(
        self,
        data: Data,
        parameters: ParameterGroup,
        options: InferenceOptions = InferenceOptions(),
    ) -> None:
        (
            projections,
            orthonormalization_matrix,
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

        hessian, coefficients = self._compute_hessian_coefficients(
            self.orthonormalization_matrix,
            self.projections,
        )

        return DiffusionMultiModelSelection(
            coefficients=self.convert_coefficients(coefficients),
            hessian=self.convert_hessian(hessian),
        )

    @partial(jax.jit, static_argnums=(0,))
    def _project_on_basis(self, data: Data, parameters: ParameterGroup):
        """
        Projects on the non-orthonormalized basis.

        """

        # Basis
        if isinstance(self.projector, ProjectorGMGS):
            basis, orthogonalized_basis = self.projector(data, parameters)
            basis_array = basis.array
            orthogonalized_basis_array = orthogonalized_basis.array

            # The real basis i.e what the real force should look like
            # basis_real = basis_array

            # The basis modified for the inference
            basis_inference = orthogonalized_basis_array
        else:
            basis = self.projector(data, parameters)
            basis_array = basis.array

            # The real basis i.e what the real force should look like
            # basis_real = basis_array
            basis_inference = basis_array

        # _, nbparticles, dof = basis_array.shape
        orthonormalization_matrix = self.projector.compute_basis_outer_product(
            None,
            basis_inference,
        )

        diffusion_projections = self._compute_diffusion_projections(
            data,
            basis_inference,
        )

        return (diffusion_projections, orthonormalization_matrix)

    @partial(jax.jit, static_argnums=(0,))
    def _compute_diffusion_projections(self, data: Data, basis_values):
        diffusion_projections = jnp.einsum(
            "i...,ai...->ia",
            self.diffusion_estimator(data),
            basis_values,
            precision=lax.Precision.HIGHEST,
        )

        return diffusion_projections

    @partial(jax.jit, static_argnums=(0))
    def _compute_hessian_coefficients(self, matrices, projections):

        inv_selected_matrix = jnp.linalg.pinv(matrices)

        orthonormalized_coefficients = _einsum(
            "...cab,...cb->...ca",
            inv_selected_matrix,
            # Mask the projections
            projections,
        )

        return -0.5 * matrices, orthonormalized_coefficients


class DiffusionNL(InferrerNL):
    __slots__ = [
        "diffusion_estimator",
    ]

    def __init__(
        self,
        projector: Projector,
        diffusion_estimator: DiffusionEstimator,
        average_inverse_diffusion,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(projector, average_inverse_diffusion, *args, **kwargs)

        self.diffusion_estimator = diffusion_estimator

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, data: Data, parameters):
        return self.projector.trajectory_integral.dispatch_sum(
            partial(minimize, method="BFGS"),
            self.cost_function,
            data,
            args=(parameters, data),
        )

    @abstractmethod
    def cost_function(self):
        pass


class DiffusionInferrerNL(DiffusionNL):
    __slots__ = []

    @partial(jax.jit, static_argnums=(0,))
    def cost_function(self, parameters, data):
        Scannee = namedtuple("Scannee", "basis_values data")

        basis_values = self.projector.compute_basis(data, parameters)

        def local_cost_func(_, scannee):
            d = jnp.einsum(
                "aijmn,jknp->ikmp",
                scannee.basis_values - self.diffusion_estimator(scannee.data),
                self.average_inverse_diffusion,
                precision=jax.lax.Precision.HIGHEST,
            )
            cost = jnp.einsum(
                "ikmp,ikmp->i",
                d,
                d,
                precision=jax.lax.Precision.HIGHEST,
            )
            return (_, cost)

        _, local_cost = jax.lax.scan(
            local_cost_func,
            None,
            Scannee(basis_values, data),
        )

        return local_cost
