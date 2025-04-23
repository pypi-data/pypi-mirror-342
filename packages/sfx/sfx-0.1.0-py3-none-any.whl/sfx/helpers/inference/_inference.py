"""Helpers for inference runs."""

__all__ = [
    "FunctionOptions",
    "FunctionParameters",
    "SamplingParameters",
    "change_timestep",
    "create_basis",
    "create_data",
    "create_functions",
    "create_parameters",
    "create_kernel",
    "create_projector",
    "create_inferrer",
    "sample_states",
    "create_states_from_dataframe",
]
import sys
from collections import namedtuple
from functools import partial
from typing import Callable, Dict, List, Optional, Tuple, Type

import jax
import jax.numpy as jnp
from jax.tree_util import Partial

from sfx.basis.basis import Basis
from sfx.basis.interactions import InteractionGroup, Interactions
from sfx.basis.parameters import ParameterGroup, Parameters
from sfx.helpers.analysis import sliding_window
from sfx.helpers.io import load
from sfx.helpers.math import compose_functions, unwrap, unwrap_lattice
from sfx.inference.data import (
    Data,
    ParticleGroup,
    TemporalGroup,
    DataGroup,
    DataGroupFunc,
)
from sfx.inference.inferrer.core import Inferrer
from sfx.inference.projector import (
    Projector,
    ProjectorGMGS,
    TrajectoryIntegral,
    TrajectoryIntegralFunc,
)
from sfx.simulate.core import SimulatePBC, SimulatePBCLattice, SimulateState


FunctionOptions = namedtuple(
    "FunctionOptions",
    "interaction_type functions kernels kernel_parameters parameters",
)

FunctionParameters = namedtuple(
    "FunctionParameters",
    "number constructor",
)

SamplingParameters = namedtuple(
    "SamplingParameters",
    "length initial_timestep inference_timestep max_nbparticles",
)


def change_timestep(old_timestep, new_timestep):
    """Change the timestep by creating a slice with a step size
    matching the ratio of int(old/new) (need old < new).
    """
    ratio = 0
    try:
        ratio = round(new_timestep / old_timestep)
        if not ratio:
            raise RuntimeError(
                f"Slice step == 0 since the new timestep"
                f" ({new_timestep}) <  old timestep ({old_timestep});"
            )

    except RuntimeError as e:
        print(e, file=sys.stderr)

    return ratio


def sample_states(states: SimulateState, step: int, width: int = 2):
    coordinates = states.coordinates[1 : -(step) - 1]
    timestep = sliding_window(
        states.time,
        step,
        width=width,
        funcs=[lambda x: jnp.diff(x, axis=0)[0]],
    )[1:-1]
    time = states.time[1 : -(step) - 1]

    if isinstance(states.pbc, SimulatePBC):
        _unwrap = unwrap
        _pbc = states.pbc[:-step]

    elif isinstance(states.pbc, SimulatePBCLattice):
        _unwrap = unwrap_lattice
        _pbc = states.pbc[:-step]
    else:
        _unwrap = lambda x, _: x
        _pbc = None

    future_motions = _unwrap(
        sliding_window(
            states.coordinates,
            step,
            width=width,
            funcs=[
                lambda x: jnp.diff(x, axis=0)[0],
            ]
            + (
                [lambda x: jnp.cross(*x[::-1])]
                if hasattr(states.coordinates, "orientation")
                else []
            ),
        ),
        _pbc,
    )[1:-1]

    past_motions = _unwrap(
        sliding_window(
            states.coordinates,
            step,
            width=width,
            funcs=[
                lambda x: jnp.diff(x[::-1], axis=0)[0],
            ]
            + (
                [
                    lambda x: jnp.cross(*x),
                ]
                if hasattr(states.coordinates, "orientation")
                else []
            ),
        ),
        _pbc,
    )[1:-1]
    velocities = (
        future_motions * jnp.reciprocal(timestep)[..., jnp.newaxis, jnp.newaxis]
    )
    nbparticles = jnp.repeat(states.nbparticles, len(states) - step - 2)
    return {
        "frame": jnp.arange(len(time)),
        "coordinates": coordinates,
        "time": time,
        "timestep": timestep,
        "future_motions": future_motions,
        "past_motions": past_motions,
        "coordinates_stratonovitch": coordinates + 0.5 * future_motions,
        "velocities": velocities,
        "nbparticles": nbparticles,
    }


def create_kernel(func, functions, parameters):
    if len(functions) != len(parameters):
        raise RuntimeError(
            "The number of functions"
            " should match the number of parameters;"
            f"Got len(functions) ({len(functions)}) !="
            f" len(parameters) ({len(parameters)})"
        )

    return compose_functions(func, *functions, parameters=parameters)


def create_functions(
    options: dict,
    parameter_name: str = "p-{i:>03d}-{j:>03d}",
    rank: int = 1,
    modifier: Partial = Partial(lambda interaction: interaction),
) -> Tuple[Dict, List, int, Partial]:
    interaction_types = []
    kernels = {}

    for field, option in options.items():
        if option is not None:
            interaction_kernels = [
                create_kernel(func, kernel, kernel_param)
                for func, kernel, kernel_param in zip(
                    option.functions,
                    option.kernels,
                    option.kernel_parameters,
                )
            ]

            interaction_parameters = [
                ParameterGroup(
                    gid=[
                        parameter_name.format(i=i, j=j)
                        for i, p in enumerate(option.parameters.number)
                        for j in range(p)
                    ],
                    grp=[
                        None
                        for _, p in enumerate(option.parameters.number)
                        for _ in range(p)
                    ],
                ),
            ]

            kernels |= {
                f"{field}": {
                    i: {"function": func, "parameters": param}
                    for i, (func, param) in enumerate(
                        zip(
                            interaction_kernels,
                            interaction_parameters,
                        )
                    )
                },
            }

            interaction_types.append(option.interaction_type)

    return kernels, interaction_types, rank, modifier


def create_parameters(
    options: dict,
    *args,
    name: str = "basis",
    parameter_name: str = "p-{i:>03d}-{j:>03d}",
    **kwargs,
):
    parameters = None

    for field, option in options.items():
        if option is not None:
            gid = [
                parameter_name.format(i=i, j=j)
                for i, p in enumerate(option.parameters.number)
                for j in range(p)
            ]

            grp = [
                param
                for parameters in option.parameters.constructor(
                    *args,
                    **kwargs,
                )
                for param in parameters
            ]

            if parameters is None:
                parameters = ParameterGroup(
                    gid=[f"{field}"],
                    grp=[ParameterGroup(gid=gid, grp=grp)],
                )
            else:
                parameters += ParameterGroup(
                    gid=[f"{field}"],
                    grp=[ParameterGroup(gid=gid, grp=grp)],
                )

    return name, parameters


def create_basis(
    kernels: dict,
    interactions_types: List[int],
    rank: int = 1,
    modifier: Partial = Partial(lambda interaction: interaction),
) -> Basis:
    kernel_list = list(kernels.items())

    first_name, first_kernels = kernel_list[0]

    gid = []
    grp = []
    for kernel in first_kernels.values():
        gid += kernel["parameters"].name
        grp += [kernel["function"] for _ in kernel["parameters"].gid]

    functions = InteractionGroup(
        gid=[first_name],
        grp=[InteractionGroup(gid=gid, grp=grp)],
    )

    for kernel_name, kernels in kernel_list[1:]:
        gid = []
        grp = []

        for kernel in kernels.values():
            gid += kernel["parameters"].name
            grp += [kernel["function"] for _ in kernel["parameters"].gid]

        functions += InteractionGroup(
            gid=[kernel_name],
            grp=[InteractionGroup(gid=gid, grp=grp)],
        )

    interactions = Interactions(
        rank=rank,
        interaction_types=interactions_types,
        functions=functions,
    )

    basis = Basis(interactions, modifier=modifier)

    return basis


def create_data(
    path: str,
    ratio: float,
    sampler: Callable = sample_states,
):
    """
    path to data
    ratio : select states points (e.g different timesteps)
    """
    states = load(path)
    if ratio != 1:
        data = Data(**sampler(states, ratio))
    else:
        data = Data(**states.to_data_input())
    return data, states[0].pbc


def create_projector(
    basis: Basis,
    trajectory_integral: TrajectoryIntegral | TrajectoryIntegralFunc,
    projection_modifier: Partial = Partial(lambda projectee: projectee._combine()),
    orthogonalizer: Optional[Basis | bool] = None,
):
    if isinstance(orthogonalizer, Basis):
        projector = ProjectorGMGS(
            basis,
            trajectory_integral,
            projection_modifier=projection_modifier,
            orthogonalizer=orthogonalizer,
        )
    elif orthogonalizer:
        projector = ProjectorGMGS(
            basis,
            trajectory_integral,
            projection_modifier=projection_modifier,
            orthogonalizer=None,
        )
    else:
        projector = Projector(
            basis,
            trajectory_integral,
            projection_modifier=projection_modifier,
        )
    return projector


def create_trajectory_integral(length, nbparticles):
    length -= 2
    nb_dit = len(str(length))
    nb_points = jnp.append(10 ** jnp.arange(nb_dit), length)
    formatter = f"{{nb:0>{nb_dit}d}}_{{type}}"

    gid = [formatter.format(nb=nb, type="consecutive") for nb in nb_points] + [
        formatter.format(nb=nb, type="sparse") for nb in nb_points[:-1]
    ]

    datagroup = DataGroup(
        gid=gid,
        grp=[
            DataGroup(
                gid=["all"],
                grp=[()],
            )
            for _ in range(len(gid))
        ],
    )

    consecutive_sampling = nb_points
    sparse_sampling = nb_points[::-1][:-1]

    @Partial
    def funcgroup(data, *args, **kwargs):
        fixed_array = jnp.ones((1, nbparticles), dtype=jnp.bool)
        return jnp.append(
            jax.vmap(lambda i: (data.frame < i) * fixed_array)(consecutive_sampling),
            jax.vmap(lambda i: (data.frame % i == 0) * fixed_array)(sparse_sampling),
            axis=0,
        )

    datagroupfunc = DataGroupFunc(datagroup=datagroup, funcgroup=funcgroup)
    trajectory_integral = TrajectoryIntegralFunc(group=datagroupfunc)

    return trajectory_integral


def create_inferrer(
    basis_options,
    sampling_parameters,
    *args,
    inferrer_type: Type[Inferrer],
    diffusion_estimator: Optional[Partial | jax.Array] = None,
    projection_modifier: Partial = Partial(lambda projectee: projectee._combine()),
    orthogonalizer_options: Optional[Dict | bool] = None,
    **kwargs,
):
    ratio = int(
        sampling_parameters.inference_timestep / sampling_parameters.initial_timestep
    )

    if ratio != 1:
        new_length = sampling_parameters.length - ratio
    else:
        new_length = sampling_parameters.length

    if isinstance(orthogonalizer_options, dict) and orthogonalizer_options:
        orthogonalizer = create_basis(*create_functions(**orthogonalizer_options))
    elif orthogonalizer_options:
        orthogonalizer = True
    else:
        orthogonalizer = None

    projector = create_projector(
        basis=create_basis(*create_functions(**basis_options)),
        trajectory_integral=create_trajectory_integral(
            new_length,
            sampling_parameters.max_nbparticles,
        ),
        projection_modifier=projection_modifier,
        orthogonalizer=orthogonalizer,
    )

    return inferrer_type(
        projector=projector,
        diffusion_estimator=diffusion_estimator,
    )


try:
    from pandas import DataFrame
except ImportError as e:
    print(e)

    def create_states_from_dataframe(*_, **__):
        del _, __
        raise NotImplementedError(
            "This function requires the pandas module but it has not been found."
        )

else:

    def create_states_from_dataframe(
        df: DataFrame,
        position_names=["x", "y", "z"],
        orientation_names=None,
    ):
        """Requires pandas"""

        column_names = df.columns

        unique_particles = df["particle"].unique()
        max_number_particles = len(unique_particles)

        unique_frames = df["frame"].unique()
        nb_frames = len(unique_frames)

        _mapping = {
            particle: index
            for particle, index in zip(
                unique_particles, jnp.arange(max_number_particles)
            )
        }

        def map_index(particle):
            return _mapping[particle]

        def get_position(df):
            return df.loc[:, position_names].to_numpy()[0]

        if "time" in column_names:
            time_column = "time"
        else:
            time_column = "frame"

        def get_time(df):
            return df[time_column].iloc[0]

        dof = len(position_names)
        time = jnp.empty(nb_frames)

        positions = jnp.full((nb_frames, max_number_particles, dof), jnp.nan)
        orientations = None

        coordinates = {}

        if orientation_names is not None:
            orientations = jnp.full(
                (nb_frames, max_number_particles, dof, dof), jnp.nan
            )

            def get_orientation(df):
                return jnp.stack(
                    [df.loc[:, on].to_numpy()[0] for on in orientation_names]
                )

            for frame in unique_frames:
                _df = df[df["frame"] == frame]

                for particle in _df.particle:
                    _index = map_index(particle)
                    _particle_df = _df[_df.particle == particle]

                    positions = positions.at[frame, _index].set(
                        get_position(_particle_df)
                    )
                    orientations = orientations.at[frame, _index].set(
                        get_orientation(_particle_df)
                    )

                time = time.at[frame].set(get_time(_df))

            orientations = jnp.true_divide(
                orientations,
                jnp.linalg.norm(orientations, axis=-1)[..., jnp.newaxis],
            )

            coordinates |= {
                "position": positions,
                "orientation": orientations,
            }

        else:
            for frame in unique_frames:
                _df = df[df["frame"] == frame]

                for particle in _df.particle:
                    _index = map_index(particle)
                    _particle_df = _df[_df.particle == particle]
                    positions = positions.at[frame, _index].set(
                        get_position(_particle_df)
                    )

                time = time.at[frame].set(get_time(_df))

            coordinates |= {"position": positions}

        return time, coordinates


# def fix_basis_names(
#     name="basis",
#     parameter_name="p-{i:>03d}-{j:>03d}",
# ):
#     return partial(
#         create_parameters,
#         name=name,
#         parameter_name=parameter_name,
#     )
