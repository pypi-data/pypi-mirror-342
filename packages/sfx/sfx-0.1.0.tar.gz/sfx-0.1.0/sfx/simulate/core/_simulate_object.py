"""Defines the base class for all simulate classes."""

__all__ = [
    "Simulate",
    "SimulateCoordinates",
    "SimulateFunctions",
    "SimulateFunctionParameters",
    "SimulateParameters",
    "SimulatePBC",
    "SimulatePBCLattice",
    "SimulateState",
]

from abc import abstractmethod

# from dataclasses import dataclass
from functools import partial
from math import prod
from types import NoneType
from typing import Callable

import jax

# from jaxlib.xla_extension import DeviceArray
import jax.numpy as jnp
from jax import lax

from sfx.core.sfx_object import SFXIterable, SFXObject
from sfx.helpers.math import get_rotation_axis, unwrap, unwrap_lattice
from sfx.utils.console.progress_bar import ProgressBarForLoop, ProgressBarScan


class SimulatePBC(SFXIterable):
    __slots__ = "min", "max"

    def __init__(
        self,
        min: jax.Array = jnp.full(1, -jnp.inf),
        max: jax.Array = jnp.full(1, jnp.inf),
    ) -> None:
        self.min = min
        self.max = max

        if isinstance(self.min, jax.Array) and self.min.ndim == 2:
            super().__init__(self.min.shape[0])
        else:
            super().__init__()


class SimulatePBCLattice(SFXIterable):
    __slots__ = "direct_lattice", "reciprocal_lattice"

    def __init__(
        self,
        direct_lattice,
        reciprocal_lattice=None,
    ) -> None:
        self.direct_lattice = direct_lattice

        if reciprocal_lattice is None:
            self.reciprocal_lattice = jnp.linalg.inv(direct_lattice)
        else:
            self.reciprocal_lattice = reciprocal_lattice

        if isinstance(self.direct_lattice, jax.Array) and self.direct_lattice.ndim == 3:
            super().__init__(self.direct_lattice.shape[0])
        else:
            super().__init__()

    @property
    def direct_volume(self):
        return jnp.linalg.det(self.direct_lattice)

    @property
    def reciprocal_volume(self):
        return jnp.linalg.det(self.reciprocal_lattice)


class SimulateFunctions(SFXObject):
    """Base Container for the simulation functions."""

    __slots__ = []


class SimulateFunctionParameters(SFXObject):
    """Base Container for the simulation function parameters."""

    __slots__ = []


class SimulateParameters(SFXObject):
    """Base class for simulation parameters."""

    __slots__ = ["oversampling"]

    def __init__(self, oversampling: int = 0):
        super().__init__()
        self.oversampling = oversampling


class SimulateCoordinates(SFXIterable):
    __slots__ = ["__dict__"]

    def __init__(self, position: jax.Array = jnp.empty((0, 0)), **kwargs):
        # This is a check for JAX PyTrees flattening and unflattening
        # Need to find a way to have this checked automatically everytime
        # we init a `SFXIterable`` subclass.
        if hasattr(position, "ndim"):
            super().__init__(position.shape[0])
            # if position.ndim == 3:
            #     super().__init__(position.shape[0])
            # else:
            #     super().__init__()

        self.__dict__.update({"position": position})
        self.__dict__.update(self._check_input(kwargs))

    def _check_input(self, kwargs):
        # We check that the values in kwargs have a 'shape'
        # attribute. This is important for JAX flattening that
        # will not necessarily pass device arrays but object.
        if any(hasattr(v, "shape") for v in kwargs.values()) and all(
            len(v.shape) > 1 for v in kwargs.values()
        ):
            if not all(
                v1.shape[0] == v2.shape[0]
                for v1 in kwargs.values()
                for v2 in kwargs.values()
            ):
                raise TypeError(
                    "Inputs should have the same length for the 1st axis; "
                    f"got ({', '.join(f'{k}={v.shape}' for k,v in kwargs.items())})"
                )
        return kwargs

    @property
    def nbparticles(self):
        # Get the number of particles using the first entry
        # Use -2 as the first axis corresponds to the steps
        # after simulation
        if self.nbdimensions >= 3:
            nbparticles = next(iter(self.__dict__.values())).shape[1]
        else:
            nbparticles = next(iter(self.__dict__.values())).shape[0]
        return nbparticles

    @property
    def dof(self):
        # Get the dof by summing the length of the last axis
        return sum(v.shape[-1] for v in self.__dict__.values())

    @property
    def nbdimensions(self):
        return next(iter(self.__dict__.values())).ndim

    @property
    def dimensions(self):
        if self.nbdimensions == 3:
            dimension = (self.length, self.nbparticles, self.dof)
        else:
            dimension = (self.nbparticles, self.dof)
        return dimension

    @property
    def offset(self):
        _offset = {}
        start = 0
        end = 0

        for k, v in self.__dict__.items():
            end += v.shape[-1]
            _offset[k] = slice(start, end)
            start += v.shape[-1]

        return _offset

    @property
    def future_motion(self):
        if self.nbdimensions == 3:

            output = jnp.zeros((self.length - 2, self.nbparticles, self.dof))

            for name, _sl in self.offset.items():
                if name == "orientation" and self[name].ndim == 4:
                    output = output.at[..., _sl].set(
                        jax.lax.scan(
                            lambda _, arrays: (
                                None,
                                jax.vmap(get_rotation_axis, in_axes=(0, 0))(
                                    arrays[0],  # Coordinates Frame Before
                                    arrays[1],  # Coordinates Frame After
                                ),
                            ),
                            None,
                            (self[name][1:-1], self[name][2:]),  # type: ignore
                        )[-1]
                    )
                else:
                    output = output.at[..., _sl].set(self[name][2:] - self[name][1:-1])  # type: ignore

        else:
            raise TypeError(
                "Coordinates should have 3 dimensions; "
                " got {self.nbdimensions} dimensions"
            )

        return self._separate(output)

    @property
    def past_motion(self):
        if self.nbdimensions == 3:

            output = jnp.zeros((self.length - 2, self.nbparticles, self.dof))

            for name, _sl in self.offset.items():
                if name == "orientation" and self[name].ndim == 4:
                    output = output.at[..., _sl].set(
                        jax.lax.scan(
                            lambda _, arrays: (
                                None,
                                jax.vmap(
                                    get_rotation_axis,
                                    in_axes=(0, 0),
                                )(
                                    arrays[0],  # Coordinates Frame Before
                                    arrays[1],  # Coordinates Frame After
                                ),
                            ),
                            None,
                            (self[name][2:], self[name][1:-1]),  # type: ignore
                        )[-1]
                    )
                else:
                    output = output.at[..., _sl].set(self[name][1:-1] - self[name][2:])  # type: ignore

        else:
            raise TypeError(
                "Coordinates should have 3 dimensions; "
                " got {self.nbdimensions} dimensions"
            )

        return self._separate(output)

    @property
    def stratonovitch(self):
        # self._separate(
        #     self._combine()[1:-1] + 0.5 * self.future_motion._combine()
        # )
        return None

    def _combine(self):
        """Combines all the attributes into one array."""
        return jnp.block(
            [
                (
                    v.reshape(self.length, self.nbparticles, -1)
                    if v.ndim >= 3
                    else v.reshape(self.nbparticles, -1)
                )
                for v in self.__dict__.values()
            ]
        )

    def _separate(self, array):
        """Separates an array back into attributes. The opposite of
        `_combine`.
        """
        if array.ndim == self.nbdimensions:
            cls = type(self)

            _temp = cls(**{k: array[..., self.offset[k]] for k in self.__dict__.keys()})
        else:
            raise TypeError(
                "The number of dimensions of the input array should "
                "match the number of dimensions of the coordinates;"
                f" got {array.ndim}, expect {self.nbdimensions}"
            )
        return _temp

    def __add__(self, other):
        cls = type(self)

        if isinstance(other, cls):
            _temp = self._combine() + other._combine()

        elif isinstance(other, jax.Array | int | float | complex):
            _temp = self._combine() + other

        else:
            raise TypeError(
                "Wrong type for addition; Expect "
                f"{cls}, jax.Array, int, float or complex. Got {type(other)}"
            )

        return self._separate(_temp)

    def __radd__(self, other):
        return self.__add__(other)

    def __ladd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __lsub__(self, other):
        return self.__sub__(other)

    def __neg__(self):
        return self._separate(-self._combine())

    def __pos__(self):
        return self._separate(self._combine())

    def __mul__(self, other):
        cls = type(self)

        if isinstance(other, cls):
            _temp = self._combine() * other._combine()

        elif isinstance(other, jax.Array | int | float | complex):
            _temp = self._combine() * other

        else:
            raise TypeError(
                "Wrong type for multiplication; Expect "
                f"{cls}, jax.Array, int, float or complex. Got {type(other)}"
            )

        return self._separate(_temp)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __lmul__(self, other):
        return self.__mul__(other)

    def __inv__(self):
        return self._separate(1 / self._combine())

    def __truediv__(self, other):
        cls = type(self)

        if isinstance(other, cls):
            _temp = self._combine() * other.__inv__()

        elif isinstance(other, jax.Array | int | float | complex):
            _temp = self._combine() / other

        else:
            raise TypeError(
                "Wrong type for true division; Expect "
                f"{cls}, jax.Array, int, float or complex. Got {type(other)}"
            )

        return self._separate(_temp)

    def __rtruediv__(self, other):
        cls = type(self)

        if isinstance(other, cls):
            _temp = other / self._combine()

        elif isinstance(other, jax.Array | int | float | complex):
            _temp = other / self._combine()

        else:
            raise TypeError(
                "Wrong type for right true division; Expect "
                f"{cls}, jax.Array, int, float or complex. Got {type(other)}"
            )

        return self._separate(_temp)

    def __ltruediv__(self, other):
        return self.__truediv__(other)


class SimulateState(SFXIterable):
    """Base class for simulation state."""

    __slots__ = [
        "coordinates",
        "timestep",
        "thermal_energy",
        "time",
        "pbc",
    ]

    def __init__(
        self,
        coordinates: SimulateCoordinates = SimulateCoordinates(),
        timestep: float = 1.0,
        thermal_energy: float = 1.0,
        time: float = 0.0,
        pbc: SimulatePBC | SimulatePBCLattice = SimulatePBC(
            min=jnp.full((1,), -jnp.inf), max=jnp.full((1,), jnp.inf)
        ),
    ):
        """Initialize the state."""

        self.coordinates = coordinates
        if coordinates.nbdimensions == 2:
            super().__init__()

        elif coordinates.nbdimensions == 3:
            super().__init__(coordinates.dimensions[0])

        else:
            raise ValueError(
                "coordinates can only have 2 or 3 dimensions. "
                f"(Current {coordinates.nbdimensions})"
            )

        self.timestep = timestep
        self.time = time

        self.thermal_energy = thermal_energy
        self.pbc = pbc

    @property
    def nbparticles(self):
        return self.coordinates.nbparticles

    @property
    def dof(self):
        return self.coordinates.dof

    @property
    def nbdimensions(self):
        return self.coordinates.nbdimensions

    def to_data_input(self):
        """Creates the initialization input for the 'sfx.inference.Data' class."""
        if self.nbdimensions == 2:
            raise TypeError(
                "States cannot be used as data because "
                "the number of dimensions is too low; "
                f"got {self.nbdimensions}, expect 3"
            )

        elif self.nbdimensions == 3:
            if self.pbc:
                if isinstance(self.pbc, SimulatePBC):
                    _unwrap = unwrap

                elif isinstance(self.pbc, SimulatePBCLattice):
                    _unwrap = unwrap_lattice
                else:
                    _unwrap = lambda x, _: x
                _pbc = self.pbc[1:-1]

            else:
                _unwrap = lambda x, _: x
                _pbc = self.pbc

            future_motions = _unwrap(self.coordinates.future_motion, _pbc)

            timestep = jnp.round(
                self.time[2:] - self.time[1:-1],
                str(self.timestep.min()).count("0"),
            )

            output = dict(
                frame=jnp.arange(len(timestep)),
                coordinates=self.coordinates[1:-1],
                time=self.time[1:-1],
                timestep=timestep,
                # self.timestep[1:-1],
                future_motions=future_motions,
                past_motions=_unwrap(self.coordinates.past_motion, _pbc),
                coordinates_stratonovitch=None,  # self.coordinates[1:-1] + 0.5 * future_motions,
                # We get the velocities by dividing the future_motions by the
                # timestep (broadcasted to match the number of dimensions of future_motions)
                velocities=future_motions
                * jnp.reciprocal(timestep)[..., jnp.newaxis, jnp.newaxis],
                nbparticles=jnp.repeat(self.nbparticles, self.length - 2),
            )

        return output


class Simulate(SFXObject):
    """Base class for simulation."""

    __slots__ = ["state", "parameters"]

    def __init__(
        self,
        state: SimulateState,
        parameters: SimulateParameters = SimulateParameters(oversampling=0),
    ) -> None:
        super().__init__()
        self.state = state
        self.parameters = parameters

    def integrate(self, niter: int, parameters: SimulateFunctionParameters):
        """Public interface to integrate the `self.state` using `self.integrator`.

        :param niter: Number of iteration to integrate over.

        :return: The States of the system when integrating.

        :note: This updates the `self.state` to the last state of the integration.
        """
        (last_state, last_parameters), states = self._integrate(
            niter, self.state, parameters
        )

        self.state = last_state
        return last_parameters, states

    @partial(jax.jit, static_argnums=(0, 1))
    def _integrate(
        self, niter: int, state: SimulateState, parameters: SimulateParameters
    ):
        """Integrates the `SimulateState` using `self.integrator`.

        :param niter: Number of iteration to integrate over.
        """

        @ProgressBarScan(
            niter,
            message=f"{self.__class__.__name__}",
            # tqdm_options={"leave": False, "ncols": 80},
        )
        def step(carry, _):
            state, parameters = carry
            # If oversampling is 0 then we use the integrator directly.
            # If not, we call the self._oversampling method to call the
            # integrator as many times as the oversampling value
            # with a new timestep equal to timestep/oversampling.
            new_state, new_parameters = lax.cond(
                self.parameters.oversampling,
                self._oversampling,
                self.integrator,
                state,
                parameters,
            )

            return (new_state, new_parameters), new_state

        (last_state, last_parameters), states = lax.scan(
            step, (state, parameters), jnp.arange(niter)
        )

        return (last_state, last_parameters), states

    @abstractmethod
    def integrator(self, state: SimulateState, parameters: SimulateFunctionParameters):
        """Classes inheriting from `Simulate` should implement their own `integrator`."""
        return state, parameters

    @partial(jax.jit, static_argnums=(0,))
    def _oversampling(
        self, state: SimulateState, parameters: SimulateFunctionParameters
    ):
        """Integrates using self.integrator on a finer temporal resolution using
        self.parameters.oversampling to increase the resolution.

        :param state: State of the system.
        """

        # We store and modify the original timestep
        timestep = state.timestep
        state.timestep = state.timestep / self.parameters.oversampling

        # This slows down the code if called oftened
        # @ProgressBarForLoop(
        #     self.parameters.oversampling,
        #     message=f"Oversampling ({self.parameters.oversampling})",
        #     tqdm_options={"leave": False},
        # )
        def step(_, val):
            state, parameters = val
            (new_state, new_parameters) = self.integrator(state, parameters)
            return (new_state, new_parameters)

        new_state, new_parameters = lax.fori_loop(
            0, self.parameters.oversampling, step, (state, parameters)
        )

        # We restore the timestep to the original value
        new_state.timestep = timestep

        return new_state, new_parameters
