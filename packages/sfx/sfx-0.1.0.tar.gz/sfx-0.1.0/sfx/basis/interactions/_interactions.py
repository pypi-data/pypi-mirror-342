""""""

__all__ = [
    "NewInteractions",
    "Interactions",
    "InteractionGradients",
    "InteractionGroup",
]

from functools import partial
from math import prod
from typing import Callable, List, Tuple

import jax
import jax.numpy as jnp
import jax.scipy as jsp
from jax.tree_util import Partial

from sfx.core.sfx_object import SFXGroup, SFXObject
from sfx.helpers.math import split_matrix

_einsum = Partial(jnp.einsum, precision=jax.lax.Precision.HIGHEST)


class InteractionGroup(SFXGroup):
    __slots__ = []

    def __init__(self, gid, grp) -> None:
        super().__init__(gid=gid, grp=grp)

    @property
    def array(self):
        """Returns the groups as a homogeneous array"""
        if self._is_numeric:
            groups = jnp.stack(self._homogenize(self._get_group(self.grp)))
        else:
            raise RuntimeError(
                "Group does not contain numerical data and cannot be homogenized as an array."
            )

        return groups

    @jax.jit
    def total_per_function(self):
        """Computes the total interaction per function (sum over the pairs, triplets, ...)."""

        return self.regroup(_einsum("fi...m->fim", self.array))

    @jax.jit
    def total_per_configuration(self):
        """Computes the total interaction per body configuration (pairs, triplets, ...)."""

        return self.regroup(
            _einsum("fi...m->i...m", self.array)[jnp.newaxis, ...],
            gid=["total"],
        )

    @jax.jit
    def total_per_interaction(self):
        """Computes the total interaction per type (sum over the functions)."""

        # We use self.total_per_function().grp to get the groups as a list, not a contiguous
        # array. Then each g contain an array that we get with g.group
        return self.regroup(
            [
                _einsum("fim->im", jnp.stack(g.group))
                for g in self.total_per_function().grp
            ]
        )

    @jax.jit
    def total_per_particle(self):
        """Computes the total interaction (sum over the types)."""
        return self.regroup(
            _einsum("fi...m->im", self.array)[jnp.newaxis, ...],
            gid=["total"],
        )

    @jax.jit
    def total_per_dof(self):
        """Computes the total per dof."""
        return self.regroup(
            _einsum("...m->m", self.array)[jnp.newaxis, ...],
            gid=["total"],
        )


class Interactions(SFXObject):
    """Base class for interactions"""

    __slots__ = ["rank", "interaction_types", "functions", "modifier"]

    def __init__(
        self,
        rank: int,
        interaction_types: List,
        functions: InteractionGroup,
        modifier: Callable = Partial(lambda interactions: interactions),
    ):
        """Initialize the interactions according using functions with
        respective parameters per interaction type.

        :param types: Numbers indicating the type of interaction.
        :param functions: Functions for each type of interaction.
        """
        super().__init__()

        if any(interaction_types) == 0 or any(interaction_types) < -1:
            raise ValueError(
                "Parameter interaction_types can only contain "
                "numbers n=-1 and/or n>0 ."
            )

        if len(interaction_types) != len(functions):
            raise ValueError(
                "The number of interaction_types should match the length of"
                " functions along the first axis;"
                f" got len(interaction_types) ({len(interaction_types)}) !="
                f" len(functions) ({len(functions)})"
            )

        self.functions = functions
        self.interaction_types = interaction_types
        self.rank = rank
        self.modifier = modifier

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, coordinates, time: float, parameters):
        """Computes all the functions for each type of interactions.

        :param coordinates: system coordinates at the current state.
        :param time: current time.
        :param parameters: Parameters for each function in each type of
        interaction.

        :return: All function values for every interaction types.

        ..
            For example if there are N particles, d dof, o_1 one-body interactions
            and o_2 two-body interactions, then the output shape will be
            (N, o_1 + o_2, d)
        """

        nbparticles = coordinates.nbparticles

        # Create the first interaction outside the loop to indicate the shape
        # for all_interactions.
        interaction_func = self._create_interaction_type(
            self.interaction_types[0], nbparticles
        )

        all_interactions = self._reshape(
            interaction_func(
                coordinates,
                time=time,
                parameters=parameters[0],
                functions=self.functions[0],
            )
        )

        interactions = [all_interactions]

        for i in range(1, len(self.functions)):
            # We loop over all the functions per interaction type along with their
            # parameters to define each interaction type. This is jitted so only
            # compiled at first call.
            interaction_func = self._create_interaction_type(
                self.interaction_types[i], nbparticles
            )

            interaction = self._reshape(
                interaction_func(
                    coordinates,
                    time=time,
                    parameters=parameters[i],
                    functions=self.functions[i],
                )
            )

            interactions.append(interaction)

        return self.modifier(self.functions.regroup(interactions))

    def _create_interaction_type(self, interaction_type, nbparticles):
        """Creates interactions by vmapping."""

        # @partial(jax.jit, static_argnames=("functions",))
        def interaction(coordinates, time, parameters, functions):
            if interaction_type == -1:
                # N-body interaction
                func = self._create_interaction(nbparticles)

            elif interaction_type > 0:
                func = self._create_interaction(interaction_type)

            return func(coordinates, time, parameters, functions)

        return interaction

    def _create_interaction(self, interaction_type):
        """Creates interactions by nesting jax.lax.scan."""

        def function(coordinates, time, parameters, functions):
            configuration = [coordinates[0]] * interaction_type

            def atomic_function(configuration, coordinates_j):
                configuration[interaction_type - 1] = coordinates_j
                return (
                    configuration,
                    self._compute_all_functions(
                        *configuration,
                        time=time,
                        parameters=parameters,
                        functions=functions,
                    ),
                )

            func = atomic_function

            for i in reversed(range(interaction_type - 1)):
                func = self._create_func(i, coordinates, func)

            return jax.lax.scan(func, configuration, coordinates)[-1]

        return function

    @staticmethod
    def _create_func(i, coordinates, func):
        def tmp(configuration, coordinates_j):
            configuration[i] = coordinates_j
            return jax.lax.scan(func, configuration, coordinates)

        return tmp

    @partial(jax.jit, static_argnums=(0,), static_argnames=("functions",))
    def _compute_all_functions(self, *args, time, parameters, functions):
        nbfunctions = len(functions)
        all_functions = functions[0](*args, time=time, parameters=parameters[0])[
            jnp.newaxis, ...
        ]

        for i in range(1, nbfunctions):
            all_functions = jnp.append(
                all_functions,
                functions[i](*args, time=time, parameters=parameters[i])[
                    jnp.newaxis, ...
                ],
                axis=0,
            )

        return all_functions

    @partial(jax.jit, static_argnums=(0,))
    def _reshape(self, array):
        """Reshapes an array such that the last axes match
        the rank of the output.
        """
        new_array = array.swapaxes(0, -self.rank - 1).swapaxes(-self.rank - 1, 1)
        new_shape = new_array.shape

        if self.rank > 1 and len(new_shape) % self.rank == 0:
            new_array = jax.vmap(
                lambda array: split_matrix(
                    jsp.linalg.block_diag(*array), *new_shape[-self.rank :]
                ),
                in_axes=0,
            )(new_array)

        return new_array

    @property
    def nbfunctions(self):
        return prod(len(it) for it in self.interaction_types)


class InteractionGradients(SFXObject):
    """Base class for interaction gradients"""

    __slots__ = ["interactions", "gradient_options"]

    def __init__(
        self,
        interactions: Interactions,
        gradient_options=dict(),
    ):
        self.interactions = interactions
        self.gradient_options = gradient_options

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, coordinates, time: float, parameters):
        gradient = jax.jacfwd(
            lambda c, t, p: self.interactions(c, t, p).group,
            **self.gradient_options,
        )(coordinates, time, parameters)

        if type(gradient) == type(coordinates):
            # Frow now we lose the possibility to select the gradient per coordinate attribute
            output = self.interactions.functions.regroup(gradient._combine())
        else:
            output = self.interactions.functions.regroup(gradient)

        return output


class NewInteractions(SFXObject):
    """Base class for interactions"""

    __slots__ = ["rank", "interaction_types", "functions", "modifier"]

    def __init__(
        self,
        rank: int,
        interaction_types: List,
        functions: Tuple[Tuple],
        modifier: Callable = Partial(lambda interactions: interactions),
    ):
        """Initialize the interactions according using functions with
        respective parameters per interaction type.

        :param types: Numbers indicating the type of interaction.
        :param functions: Functions for each type of interaction.
        """
        super().__init__()

        if any(interaction_types) == 0 or any(interaction_types) < -1:
            raise ValueError(
                "Parameter interaction_types can only contain "
                "numbers n=-1 and/or n>0 ."
            )

        if len(interaction_types) != len(functions):
            raise ValueError(
                "The number of interaction_types should match the length of"
                " functions along the first axis;"
                f" got len(interaction_types) ({len(interaction_types)}) !="
                f" len(functions) ({len(functions)})"
            )

        self.functions = functions
        self.interaction_types = interaction_types
        self.rank = rank
        self.modifier = modifier

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, coordinates, time: float, parameters):
        """Computes all the functions for each type of interactions.

        :param coordinates: system coordinates at the current state.
        :param time: current time.
        :param parameters: Parameters for each function in each type of
        interaction.

        :return: All function values for every interaction types.

        ..
            For example if there are N particles, d dof, o_1 one-body interactions
            and o_2 two-body interactions, then the output shape will be
            (N, o_1 + o_2, d)
        """

        nbparticles = coordinates.nbparticles

        # Create the first interaction outside the loop to indicate the shape
        # for all_interactions.
        interaction_func = self._create_interaction_type(
            self.interaction_types[0], nbparticles
        )

        all_interactions = self._reshape(
            interaction_func(
                coordinates,
                time=time,
                parameters=parameters[0],
                functions=self.functions[0],
            )
        )

        interactions = [all_interactions]

        for i in range(1, len(self.functions)):
            # We loop over all the functions per interaction type along with their
            # parameters to define each interaction type. This is jitted so only
            # compiled at first call.
            interaction_func = self._create_interaction_type(
                self.interaction_types[i], nbparticles
            )

            interaction = self._reshape(
                interaction_func(
                    coordinates,
                    time=time,
                    parameters=parameters[i],
                    functions=self.functions[i],
                )
            )

            interactions.append(interaction)

        return self.modifier(parameters.regroup(interactions))

    def _create_interaction_type(self, interaction_type, nbparticles):
        """Creates interactions by vmapping."""

        # @partial(jax.jit, static_argnames=("functions",))
        def interaction(coordinates, time, parameters, functions):
            if interaction_type == -1:
                # N-body interaction
                func = self._create_interaction(nbparticles)

            elif interaction_type > 0:
                func = self._create_interaction(interaction_type)

            return func(coordinates, time, parameters, functions)

        return interaction

    def _create_interaction(self, interaction_type):
        """Creates interactions by nesting jax.lax.scan."""

        def function(coordinates, time, parameters, functions):
            x = [coordinates[0]] * interaction_type

            def atomic_function(x, x_j):
                x[interaction_type - 1] = x_j
                return (
                    x,
                    self._compute_all_functions(
                        *x,
                        time=time,
                        parameters=parameters,
                        functions=functions,
                    ),
                )

            func = atomic_function

            for i in reversed(range(interaction_type - 1)):
                func = self._create_func(i, coordinates, func)

            return jax.lax.scan(func, x, coordinates)[-1]

        return function

    @staticmethod
    def _create_func(i, coordinates, func):
        def tmp(x, x_j):
            x[i] = x_j
            return jax.lax.scan(func, x, coordinates)

        return tmp

    @partial(jax.jit, static_argnums=(0,), static_argnames=("functions",))
    def _compute_all_functions(self, *args, time, parameters, functions):
        # nbfunctions = len(functions)
        #
        # all_functions = jax.vmap(functions[0], in_axes=[None] * nbargs + [0])(
        #     *args,
        #     time=time,
        #     parameters=parameters[0],
        # )[jnp.newaxis, ...]
        #
        # for i in range(1, nbfunctions):
        #     all_functions = jnp.append(
        #         all_functions,
        #         jax.vmap(functions[0], in_axes=[None] * nbargs + [0])(
        #             *args,
        #             time=time,
        #             parameters=parameters[i],
        #         )[jnp.newaxis, ...],
        #         axis=0,
        #     )
        #
        # nbargs = len(args) + 1
        # print(nbargs)
        # return jnp.vstack(
        #     [
        #         jax.vmap(functions[i], in_axes=[None] * nbargs + [0])(
        #             *args,
        #             time,
        #             p,
        #         )[jnp.newaxis, ...]
        #         for i, p in enumerate(parameters)
        #     ]
        # )
        # nbfunctions = len(functions)
        # all_functions = functions[0](*args, time=time, parameters=parameters[0])[
        #     jnp.newaxis, ...
        # ]
        #
        # for i in range(1, nbfunctions):
        #     all_functions = jnp.append(
        #         all_functions,
        #         functions[i](*args, time=time, parameters=parameters[i])[
        #             jnp.newaxis, ...
        #         ],
        #         axis=0,
        #     )

        return jnp.stack(
            [
                jnp.vstack([functions[i](*args, time=time, parameters=pp) for pp in p])
                for i, p in enumerate(parameters)
            ],
            axis=0,
        )

    @partial(jax.jit, static_argnums=(0,))
    def _reshape(self, array):
        """Reshapes an array such that the last axes match
        the rank of the output.
        """

        return array.swapaxes(0, -self.rank - 2).swapaxes(1, -self.rank - 1)

    @property
    def nbfunctions(self):
        return prod(len(it) for it in self.interaction_types)


# class InteractionGroup(SFXGroup):
#     __slots__ = []
#
#     def __init__(self, gid, grp) -> None:
#         super().__init__(gid=gid, grp=grp)
#
#     @property
#     def array(self):
#         """Returns the groups as a homogeneous array"""
#         if self._is_numeric:
#             groups = jnp.stack(self._homogenize(self._get_group(self.grp)))
#         else:
#             raise RuntimeError(
#                 "Group does not contain numerical data and cannot be homogenized as an array."
#             )
#
#         return groups
#
#     # def _regroup_array(self, array):
#     #     """Creates a group tree from a homogeneous 2D-array. Opposite operation of array."""
#     #     cls = type(self)
#     #
#     #     # Root new groups
#     #     new_groups = []
#     #     offset = 0
#     #
#     #     for i, _ in enumerate(self.gid):
#     #         current_grp = self.grp[i]
#     #         if isinstance(current_grp, jax.Array):
#     #             if current_grp.shape:
#     #                 grp_length = current_grp.shape[0]
#     #             else:
#     #                 grp_length = 1
#     #         else:
#     #             grp_length = len(current_grp)
#     #
#     #         index = slice(None, None, None)
#     #         if grp_length == 1:
#     #             index = 0
#     #
#     #         grp = array[offset : offset + grp_length]
#     #         offset += grp_length
#     #
#     #         jax.debug.print(
#     #             f"{i=}\n"
#     #             f"{type(current_grp)=}\n"
#     #             f"{grp_length=}\n"
#     #             f"{grp.shape=}\n"
#     #             f"{array.shape=}\n"
#     #             f"{offset=}\n"
#     #             f"{index=}\n"
#     #         )
#     #
#     #         if isinstance(current_grp, SFXGroup) and len(current_grp) == len(grp):
#     #             if all(isinstance(grp, SFXGroup) for grp in current_grp.grp):
#     #                 new_groups.append(current_grp._regroup_array(grp[index]))
#     #             else:
#     #                 new_groups.append(type(self.grp[i])(gid=self.grp[i].gid, grp=grp))
#     #         elif isinstance(current_grp, SFXGroup):
#     #             new_groups.append(current_grp._regroup_array(grp[index]))
#     #         else:
#     #             new_groups.append(grp[index])
#     #     return cls(gid=self.gid, grp=new_groups)
#
#     @jax.jit
#     def total_per_function(self):
#         """Computes the total interaction per function (sum over the pairs, triplets, ...)."""
#
#         return self.regroup(
#             jnp.einsum("fi...m->fim", self.array, precision=jax.lax.Precision.HIGHEST)
#         )
#
#     @jax.jit
#     def total_per_configuration(self):
#         """Computes the total interaction per body configuration (pairs, triplets, ...)."""
#
#         return self.regroup(
#             jnp.einsum(
#                 "fi...m->i...m",
#                 self.array,
#                 precision=jax.lax.Precision.HIGHEST,
#             )[jnp.newaxis, ...],
#             gid=["total"],
#         )
#
#     @jax.jit
#     def total_per_interaction(self):
#         """Computes the total interaction per type (sum over the functions)."""
#
#         # We use self.total_per_function().grp to get the groups as a list, not a contiguous
#         # array. Then each g contain an array that we get with g.group
#         return self.regroup(
#             [
#                 jnp.einsum(
#                     "fim->im",
#                     jnp.stack(g.group),
#                     precision=jax.lax.Precision.HIGHEST,
#                 )
#                 for g in self.total_per_function().grp
#             ]
#         )
#
#     @jax.jit
#     def total_per_particle(self):
#         """Computes the total interaction (sum over the types)."""
#         return self.regroup(
#             jnp.einsum("fi...m->im", self.array, precision=jax.lax.Precision.HIGHEST)[
#                 jnp.newaxis, ...
#             ],
#             gid=["total"],
#         )
#
#     @jax.jit
#     def total_per_dof(self):
#         """Computes the total per dof."""
#         return self.regroup(
#             jnp.einsum("...m->m", self.array, precision=jax.lax.Precision.HIGHEST)[
#                 jnp.newaxis, ...
#             ],
#             gid=["total"],
#         )
