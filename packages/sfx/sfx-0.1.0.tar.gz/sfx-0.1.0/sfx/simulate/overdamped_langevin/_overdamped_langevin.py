"""Defines simulate class for Overdamped Langevin Dynamics."""

__all__ = [
    "OverdampedLangevin",
    "OverdampedLangevinState",
    "OverdampedLangevinFunctions",
    "OverdampedLangevinFunctionParameters",
]

from functools import partial
from multiprocessing.dummy import Array
from typing import Callable

import jax
import jax.numpy as jnp
import jax.scipy as jsp
from jax.experimental import host_callback
from jax.tree_util import Partial

from sfx.helpers.math import (
    fix_pbc,
    fix_pbc_lattice,
    recombine_matrix,
    rotate_vector_around_axis,
)
from sfx.simulate.core import (
    Simulate,
    SimulateFunctionParameters,
    SimulateFunctions,
    SimulatePBC,
    SimulatePBCLattice,
    SimulateState,
)

_einsum = Partial(jnp.einsum, precision=jax.lax.Precision.HIGHEST)
_matmul = Partial(jnp.matmul, precision=jax.lax.Precision.HIGHEST)


class OverdampedLangevinFunctions(SimulateFunctions):
    """Functions for `OverdampedLangevin` simulation."""

    __slots__ = [
        "force",
        "mobility",
        "spurious_drift",
        "sqrt_diffusion",
        "update",
    ]

    def __init__(
        self,
        force: Partial,
        mobility: Partial,
        spurious_drift: Partial | None = None,
        sqrt_diffusion: Partial | str | None = None,
        update: Partial | None = None,
    ) -> None:
        super().__init__()
        self.force = force
        self.mobility = mobility
        self.sqrt_diffusion = sqrt_diffusion

        if spurious_drift is None:
            # The spurious drift is defined as the divergence of the diffusion
            # tensor which is equal to the gradient of the diffusion tensor
            # with its two last axis contracted with an identity matrix.
            # divD = gradD : I
            @jax.jit
            def compute_spurious_drift(coordinates, time, parameters):
                """
                divD = gradD:I = ( dD_{ij}/dx_{k} e_i X e_j X e_k ) : ( e_j X e_k )
                """

                total_dof = coordinates.nbparticles * coordinates.dof

                gradient = jax.jacfwd(
                    lambda c, time, parameters: recombine_matrix(
                        mobility(c, time, parameters).array[0]
                    )
                )(coordinates, time=time, parameters=parameters)
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

            self.spurious_drift = compute_spurious_drift

        else:
            self.spurious_drift = spurious_drift

        if update is None:

            @jax.jit
            def update_state(state, motion, parameters, key):
                if isinstance(state.pbc, SimulatePBC):
                    _fix_pbc = fix_pbc

                elif isinstance(state.pbc, SimulatePBCLattice):
                    _fix_pbc = fix_pbc_lattice

                else:
                    _fix_pbc = Partial(lambda x, _: x)
                # Compute the new state and fix the pbc
                state.coordinates.position = _fix_pbc(
                    state.coordinates.position
                    + motion[..., state.coordinates.offset["position"]],
                    state.pbc,
                )

                if "orientation" in state.coordinates:
                    state.coordinates.orientation = jax.vmap(
                        rotate_vector_around_axis, in_axes=(0, 0)
                    )(
                        state.coordinates.orientation,
                        motion[..., state.coordinates.offset["orientation"]],
                    )

                state.key = key
                state.time = state.time + state.timestep

                return state, parameters

            self.update = update_state

        else:
            self.update = update


class OverdampedLangevinFunctionParameters(SimulateFunctionParameters):
    """Parameters for `OverdampedLangevinFunctions`."""

    __slots__ = ["force", "mobility"]

    def __init__(
        self,
        force: SimulateFunctionParameters,
        mobility: SimulateFunctionParameters,
    ) -> None:
        super().__init__()
        self.force = force
        self.mobility = mobility


class OverdampedLangevinState(SimulateState):
    """Store the state for Overdamped Langevin Simulation."""

    __slots__ = ["key"]

    def __init__(self, key=jax.random.PRNGKey(42), **kwargs):
        super().__init__(**kwargs)
        self.key = key


class OverdampedLangevin(Simulate):
    """Simulate the evolution of an `OverdampedLangevinState` with `OverdampedLangevinFunctions`."""

    __slot__ = ["functions"]

    def __init__(
        self,
        state: OverdampedLangevinState,
        functions: OverdampedLangevinFunctions,
        **kwargs,
    ) -> None:
        super().__init__(state, **kwargs)
        self.functions = functions

    @partial(jax.jit, static_argnums=0)
    def integrator(
        self,
        state: OverdampedLangevinState,
        parameters: OverdampedLangevinFunctionParameters,
    ):
        """Computes the state evolution using a simple Euler scheme."""
        key, subkey = jax.random.split(state.key)
        N = state.coordinates.nbparticles
        dof = state.coordinates.dof

        # OOOOOOOOOOLD
        # self.functions.force returns all the forces, we have to sum them
        # to get the total force. The shape should be (N, nbfunctions, dof)
        # so that summing over the nbfunctions axis gives the total force
        # per particle.
        # force = jnp.nansum(
        #     self.functions.force(
        #         state.coordinates, time=state.time, parameters=parameters.force
        #     ),
        #     axis=-2,
        # )

        # The computed force is encapsulated in an InteractionGroup. To get the
        # total force, we call the total_per_particle() method followed by group to get the
        # result as a jax.Array
        force = (
            self.functions.force(
                state.coordinates, time=state.time, parameters=parameters.force
            )
            .total_per_particle()
            .array
        )
        mobility = self.functions.mobility(
            state.coordinates,
            time=state.time,
            parameters=parameters.mobility,
        )

        # Temporary
        if not isinstance(mobility, jax.Array):
            mobility = recombine_matrix(mobility.array[0])

        diffusion = state.thermal_energy * mobility

        drift = _matmul(mobility, force.flatten()).reshape((N, dof))

        spurious_drift = state.thermal_energy * self.functions.spurious_drift(
            state.coordinates, time=state.time, parameters=parameters.mobility
        ).reshape((N, dof))

        white_noise = jnp.sqrt(2 * state.timestep) * jax.random.normal(
            key=subkey, shape=(N * dof,)
        )

        # Need to convert the output of sqrtm to float since it
        # always returns complex types.
        if isinstance(self.functions.sqrt_diffusion, str):
            if self.functions.sqrt_diffusion == "diagonal":
                sqrtD = jnp.sqrt(diffusion)
            else:
                raise RuntimeError(
                    f"sqrt_diffusion can be: ...; got {self.functions.sqrt_diffusion}"
                )
        else:
            sqrtD = jnp.real(jsp.linalg.sqrtm(diffusion))

        thermal_motion = _matmul(
            sqrtD,
            white_noise,
            precision=jax.lax.Precision.HIGHEST,
        ).reshape((N, dof))

        # host_callback.id_print(drift, spurious_drift, thermal_motion)
        # Total change in coordinates : deterministic + stochastic
        motion = (drift + spurious_drift) * state.timestep + thermal_motion

        state, parameters = self.functions.update(state, motion, parameters, key)

        return state, parameters
