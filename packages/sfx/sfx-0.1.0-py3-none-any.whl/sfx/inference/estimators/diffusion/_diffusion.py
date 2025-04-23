""""""

__all__ = [
    "DiffusionAnsatz",
    "DiffusionEstimator",
    "DiffusionFunction",
    "DiffusionConstant",
    "DiffusionMSD",
    "DiffusionVestergaard",
    "DiffusionWeakNoise",
]

from abc import abstractmethod
from collections.abc import Callable
from functools import partial
from typing import Any

import jax
import jax.numpy as jnp
from jax import lax
from jax.tree_util import Partial

from sfx.basis.interactions import InteractionGroup
from sfx.basis.parameters import ParameterGroup
from sfx.core.sfx_object import SFXObject
from sfx.helpers.format import vmap_function
from sfx.helpers.math import split_matrix
from sfx.inference.data import Data
from sfx.simulate.core import SimulateCoordinates

# from jaxlib.xla_extension import jax.Array


class DiffusionEstimator(SFXObject):
    TypeModifier = Callable[[SimulateCoordinates], jax.Array]
    __slots__ = ["evaluation_point", "modifier"]

    def __init__(self, modifier: TypeModifier | None = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if modifier is None:

            @Partial
            def default_modifier(array: SimulateCoordinates):
                return array._combine()

            self.modifier = default_modifier
        else:
            self.modifier = modifier

        self.evaluation_point = "coordinates"

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, data: Data, *args, **kwargs):
        return self._estimate_diffusion(data, *args, **kwargs)

    @abstractmethod
    def _estimate_diffusion(self, data: Data, *args, **kwargs):
        pass


class DiffusionConstant(DiffusionEstimator):
    """Constant Estimator for the diffusion."""

    __slots__ = ["value"]

    def __init__(self, value, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = value
        self.evaluation_point = "coordinates"

    @partial(jax.jit, static_argnums=(0,))
    def _estimate_diffusion(self, data: Data):
        return split_matrix(self.value, data.coordinates.dof, data.coordinates.dof)


class DiffusionFunction(DiffusionEstimator):
    """Local-in-time estimator for the diffusion using a function."""

    TypeFunction = Callable[[SimulateCoordinates, float], jax.Array]
    __slots__ = ["function"]

    def __init__(self, function: Callable, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.function = function
        self.evaluation_point = "coordinates"

    @partial(jax.jit, static_argnums=(0,))
    def _estimate_diffusion(self, data: Data, *args, **kwargs):
        return self.function(data, *args, **kwargs)


class DiffusionAnsatz(DiffusionEstimator):
    """Local-in-time estimator for the diffusion using an ansatz."""

    _TypeFunction = Callable[[Data, ParameterGroup, Any], InteractionGroup]
    __slots__ = ["ansatz"]

    def __init__(self, ansatz: _TypeFunction, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ansatz = ansatz
        self.evaluation_point = "coordinates"

    @partial(jax.jit, static_argnums=(0,))
    def _estimate_diffusion(
        self,
        data: Data,
        parameters: ParameterGroup,
        coefficients: Any,
    ):
        return self.ansatz(data, parameters, coefficients)


class DiffusionMSD(DiffusionEstimator):
    """Local-in-time Mean Square Displacement estimator for the diffusion."""

    __slots__ = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.evaluation_point = "coordinates"

    @partial(jax.jit, static_argnums=(0,))
    def _estimate_diffusion(self, data: Data):
        flat_future_motions = self.modifier(data.future_motions).flatten()

        return split_matrix(
            0.5 * jnp.outer(flat_future_motions, flat_future_motions) / data.timestep,
            data.coordinates.dof,
            data.coordinates.dof,
        )


class DiffusionVestergaard(DiffusionEstimator):
    """Local-in-time estimator for the diffusion from [Vestergaard2014].

    [Vestergaard2014] Christian L. Vestergaard, Paul C. Blainey,
    and Henrik Flyvbjerg, Phys. Rev. E 89, 022726
    """

    __slots__ = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.evaluation_point = "coordinates"

    @partial(jax.jit, static_argnums=(0,))
    def _estimate_diffusion(self, data: Data):
        # We flatten the combined coordinates to get an (Nxdof)x(Nxdof)
        # matrix.
        future_motions = self.modifier(data.future_motions).flatten()

        past_motions = self.modifier(data.past_motions).flatten()

        return split_matrix(
            0.25
            * (
                jnp.outer(
                    future_motions + past_motions,
                    future_motions + past_motions,
                )
                + jnp.outer(future_motions, past_motions)
                + jnp.outer(past_motions, past_motions)
            )
            / data.timestep,
            data.coordinates.dof,
            data.coordinates.dof,
        )


class DiffusionWeakNoise(DiffusionEstimator):
    """Local-in-time estimator for the diffusion from [Vestergaard2014].

    [Vestergaard2014] Christian L. Vestergaard, Paul C. Blainey,
    and Henrik Flyvbjerg, Phys. Rev. E 89, 022726
    """

    TypeVelocityAnsatz = Callable[[Data], jax.Array]

    __slots__ = ["_velocity_ansatz"]

    def __init__(self, velocity_ansatz: TypeVelocityAnsatz, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.velocity_ansatz = velocity_ansatz
        self.evaluation_point = "coordinates_stratonovitch"

    @property
    def velocity_ansatz(self):
        return self._velocity_ansatz

    @velocity_ansatz.setter
    def velocity_ansatz(self, velocity_ansatz):
        if isinstance(velocity_ansatz, TypeVelocityAnsatz):
            self._velocity_ansatz = velocity_ansatz

        else:
            raise ValueError(
                "velocity_ansatz must be a function of type "
                f"{self.__class__.TypeVelocityAnsatz} or None; "
                "got {type(velocity_ansatz)}"
            )

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, data: Data):
        # We flatten the combined coordinates to get an (Nxdof)x(Nxdof)
        # matrix.
        future_motions = data.future_motions._combine()

        drift_corrected_motions = (
            future_motions
            - self.velocity_ansatz(data.coordinates_stratonovitch) * data.timestep
        ).flatten()

        return split_matrix(
            0.5
            * jnp.outer(drift_corrected_motions, drift_corrected_motions)
            / data.timestep,
            data.coordinates.dof,
            data.coordinates.dof,
        )
