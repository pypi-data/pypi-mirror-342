__all__ = [
    "DriftAnsatz",
    "DriftCoefficients",
    "DriftError",
    "DriftInformation",
    "DriftStratonovitchInferrer",
    "DriftItoInferrer",
    "DriftItoInferrerNL",
]

from collections import namedtuple
from collections.abc import Callable
from functools import partial
from math import prod

import jax
import jax.numpy as jnp
import jax.scipy as jsp
from jax import lax
from jax.scipy.optimize import minimize

from sfx.basis.basis import Basis
from sfx.basis.interactions import Interactions
from sfx.basis.parameters import ParameterGroup, Parameters
from sfx.core.sfx_object import SFXCallable, SFXIterable
from sfx.helpers.math import recombine_matrix, split_matrix
from sfx.inference.data import Data
from sfx.inference.estimators.diffusion import DiffusionEstimator
from sfx.inference.inferrer.core import (
    Ansatz,
    Coefficients,
    InferenceOptions,
    Inferrer,
    InferrerNL,
)
from sfx.inference.inferrer.diffusion import DiffusionAnsatz
from sfx.inference.projector import Projector, TrajectoryIntegral
from sfx.inference.statistics import Statistics

_einsum = partial(jnp.einsum, precision=jax.lax.Precision.HIGHEST)


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


class DriftDiffusionInferrerL(SFXCallable):
    __slots__ = [
        "force_basis",
        "diffusion_basis",
        "spurious_drift_basis",
        "trajectory_integral",
        "local_cost_function",
        "optimization_result",
    ]

    def __init__(
        self,
        force_basis: Basis,
        diffusion_basis: Basis,
        spurious_drift_basis: None,
        trajectory_integral: TrajectoryIntegral,
        local_cost_function=None,
        optimization_result=None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.force_basis = force_basis
        self.diffusion_basis = diffusion_basis
        self.spurious_drift_basis = spurious_drift_basis
        self.local_cost_function = local_cost_function
        self.optimization_result = optimization_result

    def __call__(self, data: Data, parameters: ParameterGroup):
        diff_func, diff_args, recombine = make_func_differentiable(
            self.cost_function, parameters, data
        )

        self.optimization_result = self._minimize(diff_func, data, diff_args)

        self.parameters = self.projector.trajectory_integral.map(
            lambda opt_res: recombine(opt_res.x),
            self.optimization_result,
        )

        self.errors = self.projector.trajectory_integral.map(
            lambda opt_res: recombine(2 * jnp.sqrt(jnp.diag(opt_res.hess_inv))),
            self.optimization_result,
        )

    @abstractmethod
    def _minimize(self, cost_function: Callable, data: Data, parameters: jax.Array):
        return None

    @abstractmethod
    def cost_function(self):
        pass

    @jax.jit
    def compute_spurious_drift(self, data, parameters):
        """
        divD = gradD:I = ( dD_{ij}/dx_{k} e_i X e_j X e_k ) : ( e_j X e_k )
        """

        total_dof = data.coordinates.nbparticles * data.coordinates.dof

        gradient = jax.jacfwd(
            lambda c, time, parameters: recombine_matrix(
                self.diffusion_basis(c, time, parameters).array[0]
            )
        )(data.coordinates, time=data.time, parameters=parameters)
        # We get the gradient wrt to all the coordinate types by
        # combining the coordinate types (since coordinates
        # is a `SimulateCoordinates` object).
        # nan_to_num in case there some singularities w.r.t to division
        # when it computes
        tmp_gradient = jnp.nan_to_num(
            gradient._combine().reshape(total_dof, total_dof, -1)
        )

        # if "orientation" in coordinates:
        #    tmp_gradient = jnp.append(
        #        tmp_gradient, gradient.orientation, axis=-1
        #    )

        return _einsum(
            "abm,bm",
            tmp_gradient,
            jnp.eye(coordinates.nbparticles * coordinates.dof),
        )
