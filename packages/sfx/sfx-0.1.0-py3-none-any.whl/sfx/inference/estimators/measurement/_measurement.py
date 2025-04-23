__all__ = ["MeasurementErrorEstimator"]

from collections.abc import Callable
from functools import partial
from types import NoneType

import jax
from jax import lax
import jax.numpy as jnp

# from jaxlib.xla_extension import DeviceArray

from sfx.core.sfx_object import SFXObject

from sfx.inference.data import Data


class MeasurementErrorEstimator(SFXObject):
    TypeVelocityAnsatz = Callable[[Data], jax.Array]

    __slots__ = ["_velocity_ansatz", "_use_velocity"]

    def __init__(
        self, velocity_ansatz: TypeVelocityAnsatz | None = None
    ) -> None:
        super().__init__()
        self.velocity_ansatz = velocity_ansatz

    @property
    def velocity_ansatz(self):
        return self._velocity_ansatz

    @velocity_ansatz.setter
    def velocity_ansatz(self, velocity_ansatz: TypeVelocityAnsatz):
        if isinstance(velocity_ansatz, TypeVelocityAnsatz):
            self._velocity_ansatz = velocity_ansatz
            self._use_velocity = True

        elif velocity_ansatz is None:
            self._velocity_ansatz = lambda data: 0.0
            self._use_velocity = False

        else:
            raise ValueError(
                "velocity_ansatz must be a function of type "
                f"{self.__class__.TypeVelocityAnsatz} or None; "
                "got {type(velocity_ansatz)}"
            )

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, data: Data):
        """
        Lambda term is a Local estimator for the measurement
        error. It is valid only in the weak drift limit;
        specifically, if eta is the random localization error, then

        <Lambda_munu> = <eta_mu eta_nu> - dt^2 <F_mu F_nu>

        i.e. it results in an underestimate (and can even be
        negative) if dt is large.

        """
        noise_estimator = 0.5 * (
            -jnp.einsum("im,in->imn", data.future_motions, data.past_motions)
            + jnp.einsum("im,in->imn", data.future_motions, data.past_motions)
        )

        drift_correction = lax.cond(
            self._use_velocity,
            self._velocity_correction,
            lambda data: 0.0,
            data,
        )

        return noise_estimator + drift_correction

    @partial(jax.jit, static_argnums=(0,))
    def _velocity_correction(self, data: Data):
        velocity = self.velocity_ansatz(data.coordinates)
        return (
            jnp.einsum("im,in->imn", velocity, velocity) * data.timestep**2
        )
