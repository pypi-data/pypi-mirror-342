""""""

__all__ = [
    "Projector",
    "ProjectorGMGS",
    "TrajectoryIntegral",
    "OrthonormalizationMatrix",
    "TrajectoryIntegralFunc",
]

from collections import namedtuple
from collections.abc import Callable
from functools import partial
from typing import Optional

import jax
import jax.numpy as jnp
import jax.scipy as jsp
from jax import lax
from jax.tree_util import Partial

from sfx.basis.basis import Basis
from sfx.basis.interactions import InteractionGroup
from sfx.basis.parameters import ParameterGroup
from sfx.core.sfx_object import SFXGroup, SFXObject
from sfx.helpers.format import make_func_differentiable
from sfx.helpers.math import (
    group_iterative_mgs,
    group_iterative_mgs_orthogonalizer,
    homogeneous_multiplication,
)
from sfx.inference.data import (
    Data,
    DataGroup,
    ParticleGroup,
    TemporalGroup,
    DataGroupFunc,
)
from sfx.utils.console.progress_bar import ProgressBarScan
from sfx.helpers.sharding import shard_sum_function, create_mesh

_einsum = Partial(jnp.einsum, precision=jax.lax.Precision.HIGHEST)


class TrajectoryIntegral(SFXObject):
    """Empirical Inner Product."""

    __slots__ = [
        "temporal_group",
        "particle_group",
    ]

    def __init__(
        self, *, temporal_group: TemporalGroup, particle_group: ParticleGroup
    ) -> None:
        self.temporal_group = temporal_group
        self.particle_group = particle_group

    @partial(jax.jit, static_argnums=(1,), static_argnames=("message",))
    def average(
        self,
        func,
        data,
        *args,
        message: str = "Averaging over trajectory",
        **kwargs,
    ):
        return jax.tree_util.tree_map(
            lambda value: self._regroup(value.grp),
            self.time_average_group(func, data, *args, message=message, **kwargs),
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

    @partial(jax.jit, static_argnums=(1,), static_argnames=("message",))
    def integrate(
        self,
        func,
        data,
        *args,
        message: str = "Integrating over trajectory",
        **kwargs,
    ):
        return jax.tree_util.tree_map(
            lambda value: self._regroup(value.grp),
            self.time_integrate_group(func, data, *args, message=message, **kwargs),
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

    @partial(jax.jit, static_argnums=(1,), static_argnames=("message",))
    def sum(
        self,
        func,
        data,
        *args,
        message: str = "Summing over trajectory",
        **kwargs,
    ):
        return jax.tree_util.tree_map(
            lambda value: self._regroup(value.grp),
            self.time_sum_group(func, data, *args, message=message, **kwargs),
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

    @partial(jax.jit, static_argnums=(1,), static_argnames=("message",))
    def sum_func(
        self,
        func,
        data,
        *args,
        message: str = "Summing over trajectory",
        **kwargs,
    ):
        return jax.tree_util.tree_map(
            lambda value: self._regroup(value),
            self.time_sum_group_func(func, data, *args, message=message, **kwargs),
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

    @partial(jax.jit, static_argnums=(1, 2))
    def dispatch_average(
        self,
        outer_func,
        inner_func,
        data,
        args=tuple(),
        kwargs=dict(),
    ):
        return self._dispatch(
            self._patch_average,
            outer_func,
            inner_func,
            data,
            args,
            kwargs,
            message="Averaging over",
        )

    @partial(jax.jit, static_argnums=(1, 2))
    def dispatch_integrate(
        self,
        outer_func,
        inner_func,
        data,
        args=tuple(),
        kwargs=dict(),
    ):
        return self._dispatch(
            self._patch_integrate,
            outer_func,
            inner_func,
            data,
            args,
            kwargs,
            message="Integrating over",
        )

    @partial(jax.jit, static_argnums=(1, 2))
    def dispatch_sum(
        self,
        outer_func,
        inner_func,
        data,
        args=tuple(),
        kwargs=dict(),
    ):
        return self._dispatch(
            self._patch_sum,
            outer_func,
            inner_func,
            data,
            args,
            kwargs,
            message="Summing over",
        )

    # AVERAGING #
    @partial(jax.jit, static_argnums=(1,))
    def _particle_average_group(self, func, carry, x):
        values = func(*x, **carry)
        return jax.tree_util.tree_map(
            lambda values: self.particle_group.average(
                jnp.ones(values.shape[0]),
                values,
                axes=(0,),
            ),
            values,
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

    @partial(jax.jit, static_argnums=(1,))
    def _inner_time_average_group(self, func, carry, x):
        values = self._particle_average_group(func, carry, x)
        return carry, values

    @partial(jax.jit, static_argnums=(1,), static_argnames=("message",))
    def time_average_group(
        self, func, data, *args, message: str = "Time Average", **kwargs
    ):
        @ProgressBarScan(
            len(data),
            message=message,
            tqdm_options={"leave": True, "ncols": 80},
        )
        def local_in_time_func(carry, x):
            return self._inner_time_average_group(func, carry, x)

        integrand = jax.lax.scan(
            local_in_time_func,
            kwargs,
            (jnp.arange(len(data)), data, *args),
        )[-1]

        return jax.tree_util.tree_map(
            lambda integrand: self.temporal_group.average(
                data.timestep,
                integrand.grp,
                axes=(0,),
            ),
            integrand,
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

    ## DISPATCHED
    @partial(jax.jit, static_argnums=(1,), static_argnames=("kwargs",))
    def _patch_average(
        self,
        func,
        groups,
        data,
        args,
        kwargs,
    ):
        def patch_averaged_inner_func(*args):
            return jnp.nansum(
                groups.temporal._group_weight(
                    groups.temporal,
                    data.timestep,
                    groups.particle._group_weight(
                        groups.particle,
                        jnp.ones(groups.particle.grp.shape[0]),
                        func.inner(*args),
                        axes=(1,),
                    ),
                    axes=(0,),
                ),
                axis=(0, 1),
            )

        return func.outer(
            patch_averaged_inner_func,
            args[0],
            # For now the first argument is the one we make differentiable
            # that's why we exclude if here with the [1:] slice.
            args[1:],
            **kwargs,
        )

    # INTEGRATION #
    @partial(jax.jit, static_argnums=(1,))
    def _particle_integrate_group(self, func, carry, x):
        values = func(*x, **carry)
        return jax.tree_util.tree_map(
            lambda values: self.particle_group.integrate(
                jnp.ones(values.shape[0]), values, axes=(0,)
            ).array,
            values,
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

    @partial(jax.jit, static_argnums=(1,))
    def _inner_time_integrate_group(self, func, carry, x):
        # data_per_timestep = x
        values = self._particle_integrate_group(func, carry, x)
        return carry, values

    @partial(jax.jit, static_argnums=(1,), static_argnames=("message",))
    def time_integrate_group(
        self,
        func,
        data,
        *args,
        message: str = "Time Integration",
        **kwargs,
    ):
        def local_in_time_func(carry, x):
            return self._inner_time_integrate_group(func, carry, x)

        if message:
            scan_args = (jnp.arange(len(data)), data, *args)
            _progress_bar = ProgressBarScan(
                len(data),
                message=message,
                tqdm_options={"leave": True, "ncols": 80},
            )
            scan_func = _progress_bar(local_in_time_func)
        else:
            scan_args = (data, *args)
            scan_func = local_in_time_func

        integrand = jax.lax.scan(scan_func, kwargs, scan_args)[-1]

        return jax.tree_util.tree_map(
            lambda integrand: self.temporal_group.integrate(
                data.timestep,
                integrand,
                axes=(0,),
            ),
            integrand,
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

    @partial(jax.jit, static_argnums=(1,), static_argnames=("message",))
    def time_sum_group(
        self,
        func,
        data,
        *args,
        message: str = "Time Summation",
        **kwargs,
    ):
        def local_in_time_func(carry, x):
            return self._inner_time_integrate_group(func, carry, x)

        if message:
            scan_args = (jnp.arange(len(data)), data, *args)
            _progress_bar = ProgressBarScan(
                len(data),
                message=message,
                tqdm_options={"leave": True, "ncols": 80},
            )
            scan_func = _progress_bar(local_in_time_func)
        else:
            scan_args = (data, *args)
            scan_func = local_in_time_func

        summand = jax.lax.scan(scan_func, kwargs, scan_args)[-1]

        return jax.tree_util.tree_map(
            lambda summand: self.temporal_group.integrate(
                jnp.ones_like(data.timestep),
                summand,
                axes=(0,),
            ),
            summand,
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

    @partial(jax.jit, static_argnums=(1,))
    def _particle_integrate_group_func(self, func, carry, x):
        values = func(*x, **carry)
        return self.particle_group.integrate_func(
            lambda *x: x,
            jnp.ones(values[0].shape[0]),
            values,
            {},
        )

    @partial(jax.jit, static_argnums=(1,))
    def _inner_time_integrate_group_func(self, func, carry, x):
        values = self._particle_integrate_group_func(func, carry, x)
        return jax.tree_util.tree_map(
            lambda v: v.grp,
            values,
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

    @partial(jax.jit, static_argnums=(1,), static_argnames=("message",))
    def time_sum_group_func(
        self,
        func,
        data,
        *args,
        message: str = "Time Summation",
        **kwargs,
    ):
        def local_in_time_func(*args, **kwargs):
            return self._inner_time_integrate_group_func(func, kwargs, args)

        output = self.temporal_group.integrate_func(
            local_in_time_func,
            jnp.ones(len(data)),
            (data, *args),
            kwargs,
            message=message,
        )
        return output  # .grp

    ## DISPATCHED INTEGRATE
    @partial(jax.jit, static_argnums=(1,), static_argnames=("kwargs",))
    def _patch_integrate(
        self,
        func,
        groups,
        data,
        args,
        kwargs,
    ):
        def patch_integrated_inner_func(*args):
            return jnp.nansum(
                groups.temporal._group_integrand(
                    groups.temporal,
                    data.timestep,
                    groups.particle._group_integrand(
                        groups.particle,
                        jnp.ones(groups.particle.grp.shape[0]),
                        func.inner(*args),
                        axes=(1,),
                    ),
                    axes=(0,),
                ),
                axis=(0, 1),
            )

        return func.outer(
            patch_integrated_inner_func,
            args[0],
            # For now the first argument is the one we make differentiable
            # that's why we exclude if here with the [1:] slice.
            args[1:],
            **kwargs,
        )

    ## SUM
    @partial(jax.jit, static_argnums=(1,), static_argnames=("kwargs",))
    def _patch_sum(
        self,
        func,
        groups,
        _,
        args,
        kwargs,
    ):
        def patch_summed_inner_func(*args):
            return jnp.nansum(
                groups.temporal._group_integrand(
                    groups.temporal,
                    jnp.ones(groups.temporal.grp.shape[0]),
                    groups.particle._group_integrand(
                        groups.particle,
                        jnp.ones(groups.particle.grp.shape[0]),
                        func.inner(*args),
                        axes=(1,),
                    ),
                    axes=(0,),
                ),
                axis=(0, 1),
            )

        return func.outer(
            patch_summed_inner_func,
            args[0],
            # For now the first argument is the one we make differentiable
            # that's why we exclude if here with the [1:] slice.
            args[1:],
            **kwargs,
        )

    # DISPATCH GENERIC FUNCTION
    @partial(
        jax.jit,
        static_argnums=(1, 2, 3),
        static_argnames=("message",),
    )
    def _dispatch(
        self,
        dispatched_func: Callable,
        outer_func: Callable,
        inner_func: Callable,
        data,
        args=tuple(),
        kwargs=dict(),
        message: str = "",
    ):
        Carry = namedtuple(
            "Carry",
            "data args kwargs temporal_group",
            defaults=[None] * 3,
        )

        Funcs = namedtuple(
            "Funcs",
            "inner outer",
            defaults=[None] * 2,
        )

        Groups = namedtuple(
            "Groups",
            "temporal particle",
            defaults=[None] * 2,
        )

        nb_temporal_group = len(self.temporal_group)
        nb_particle_group = len(self.particle_group)

        @ProgressBarScan(
            nb_particle_group,
            message=f"{message} particle groups",
            tqdm_options={"leave": True},
        )
        def inner_scan_func(carry, x):
            (particle_group,) = x
            result = dispatched_func(
                Funcs(inner=inner_func, outer=outer_func),
                Groups(temporal=carry.temporal_group, particle=particle_group),
                data,
                carry.args,
                carry.kwargs,
            )
            return (carry, result)

        @ProgressBarScan(
            nb_temporal_group,
            message=f"{message} temporal groups",
            tqdm_options={"leave": True},
        )
        def outer_scan_func(carry, x):
            (temporal_group,) = x
            _, result = jax.lax.scan(
                inner_scan_func,
                Carry(
                    data=carry.data,
                    args=carry.args,
                    kwargs=carry.kwargs,
                    temporal_group=temporal_group,
                ),
                (
                    jnp.arange(nb_particle_group),
                    self.particle_group,
                ),
            )
            return (carry, result)

        _, result = jax.lax.scan(
            outer_scan_func,
            Carry(data=data, args=args, kwargs=kwargs),
            (jnp.arange(nb_temporal_group), self.temporal_group),
        )

        flat, tree = jax.tree_util.tree_flatten(result)

        return self._regroup(
            [
                [
                    # Separate the result
                    jax.tree_util.tree_unflatten(
                        tree, [flat[k][i, j] for k, _ in enumerate(flat)]
                    )
                    for j, _ in enumerate(self.particle_group)
                ]
                for i, _ in enumerate(self.temporal_group)
            ]
        )

    def _regroup(self, groups):
        temporal_group_cls = type(self.temporal_group)
        particle_group_cls = type(self.particle_group)

        return temporal_group_cls(
            self.temporal_group.gid,
            [particle_group_cls(self.particle_group.gid, tg) for tg in groups],
        )

    def map(self, func, *mappable, **kwargs):
        # def map(self, func, mappable, *args, **kwargs):
        """"""
        _cls = type(self)
        return self._regroup(
            [
                [
                    func(
                        _cls(temporal_group=tg, particle_group=pg),
                        *(map[i][j] for map in mappable),
                        **kwargs,
                    )
                    for j, pg in enumerate(self.particle_group)
                ]
                for i, tg in enumerate(self.temporal_group)
            ]
        )


class TrajectoryIntegralFunc(SFXObject):
    """Empirical Inner Product."""

    __slots__ = ["group"]

    def __init__(self, *, group: DataGroupFunc) -> None:
        self.group = group

    @partial(
        jax.jit,
        static_argnums=(1,),
        static_argnames=("mesh", "axis_name", "update_func"),
    )
    def sum(
        self,
        func,
        *args,
        mesh=create_mesh("time"),
        axis_name="time",
        update_func=Partial(lambda *_, **kwargs: kwargs),
        **kwargs,
    ):

        @partial(shard_sum_function, mesh=mesh, axis_name=axis_name)
        def _sharded_summed_func(*args, **kwargs):

            mask = self.group.funcgroup(*args, **kwargs)
            values = func(*args, **kwargs)

            masked_values = jax.tree_util.tree_map(
                lambda value: jnp.tensordot(mask, value, axes=1),
                values,
            )
            new_kwargs = update_func(*args, **kwargs)

            return new_kwargs, masked_values

        return jax.tree_util.tree_map(
            lambda sum: self.group.regroup(sum),
            _sharded_summed_func(*args, **kwargs)[-1],
        )


class OrthonormalizationMatrix(SFXGroup):
    __slots__ = []

    def __init__(
        self, gid=None, grp=None, interactions: InteractionGroup | None = None
    ) -> None:
        if interactions is not None:
            outer_product = interactions * interactions
            super().__init__(gid=outer_product.gid, grp=outer_product.grp)

        elif gid is not None and grp is not None:
            super().__init__(gid=gid, grp=grp)

        else:
            raise RuntimeError(
                f"Initialising {type(self)} requires either gid and grp are not None or interactions is not None;"
                f"Got:\ngid={gid}\ngrp={grp}\ninteractions={interactions}\n"
            )

    @property
    def array(self):
        """Creates a homogeneous 2D-array from a group tree.

        Indices:
            |1, 2|, |5|
            |3, 4|, |6|
            [7, 8], [9]

        Size:
            [2,2], [2,1]
            [1,2], [1,1]
        """
        groups = jnp.stack(self._homogenize(self._get_group(self.grp)))

        # The groups are stacked such that the dimension of the block matrix
        # is sqrt(len(groups)). However the elements are not orderered in a row
        # or column-wise manner. Instead they are ordered in blocks in which the
        # elements are then ordered row-wise.
        # In order to reconstruct a block-matrix, care must be taken, as done below

        start = 0
        end = 0
        counter = 0
        new_groups = []

        # This loops over the first dimension (interaction types)
        for t1 in self.grp:
            # This loops over the 2nd dimension (interaction types)
            blocks = []
            for t2 in t1.grp:
                start = end

                # Loops over the functions in the 2nd dimension
                for f1 in t2.grp:
                    end += len(f1)

                # A Matrix block is constructed by slicing the groups list
                # based on the number of functions. It is then splitted
                # by the number of functions.
                blocks.append(jnp.stack(jnp.split(groups[start:end], len(t2))))
            new_groups.append(jnp.concatenate(blocks, axis=1))

        return jnp.concatenate(new_groups, axis=0)

    def _regroup_array(self, groups):
        """Creates a group tree from a homogeneous 2D-array. Opposite operation of array."""
        assert isinstance(
            groups, jax.Array
        ), f"regroup support only homogeneous arrays as arguments; got {type(groups)}"
        cls = type(self)

        # Root new groups
        t1_new_groups = []

        # Row index offset
        index_offset = 0
        index_update_counter = 0

        # This loops over the 2nd dimension (interaction types)
        for t1 in self.grp:
            t2_new_groups = []

            # Slice start on the columns
            col_start = 0

            # This loops over the 3rd dimension (function of the 1st interaction type dimension)
            for t2 in t1.grp:
                f1_new_groups = []

                index_update_counter += 1

                # This loops over the 4th dimension (function of the 2nd interaction type dimension)
                for i, f1 in enumerate(t2.grp):
                    # Slice end on the columns
                    col_end = col_start + len(f1)

                    # Index for the row
                    row_index = index_offset + i

                    # print(
                    #    t1.name,
                    #    t2.name,
                    #    f1.name,
                    #    index_update_counter,
                    #    f"{row_index}, {col_start}:{col_end}",
                    #    sep=" || ",
                    # )
                    f1_new_groups.append(
                        type(f1)(
                            gid=f1.gid,
                            grp=groups[row_index, col_start:col_end],
                        )
                    )

                if index_update_counter == len(t1):
                    index_update_counter = 0
                    index_offset += len(t2)

                t2_new_groups.append(type(t2)(gid=t2.gid, grp=f1_new_groups))

                col_start += len(f1)

            t1_new_groups.append(type(t1)(gid=t1.gid, grp=t2_new_groups))

        return cls(gid=self.gid, grp=t1_new_groups)

    @property
    def inverse(self):
        """
        Computes the inverse of the orthonormalization matrix.
        If it is actually a tensor of rank > 2. The dimensions
        not corresponding the orthonormalization are considered
        has blocks over which to compute the inverse.
        """

        array = self.array
        shape = array.shape

        # If the orthonormalization tensor is not a matrix
        # but has a rank higher than 2, flatten the last dimensions.
        if len(shape) > 2:
            newshape = [s for s in shape[:2]] + [-1]
            # Transpose the last dimension at the begining to compute the inverse by blocks
            new_array = array.reshape(*newshape).transpose(2, 0, 1)

            output = (
                jnp.linalg.pinv(new_array, hermitian=True)
                .transpose(1, 2, 0)
                .reshape(*shape)
            )
        else:
            output = jnp.linalg.pinv(array, hermitian=True)

        # Compute the inverse, transpose back, reshape back and finally regroup
        return self.regroup(output)

    def __matmul__(self, other):
        _cls = type(self)

        assert isinstance(other, (_cls, InteractionGroup)), str(
            f"Right-side for matrix multiplication should be of the same type {_cls.__name__} or {InteractionGroup.__name__}; "
            f" Got {_cls.__name__} @ {type(other).__name__}"
        )

        self_array: jax.Array = self.array
        other_array: jax.Array = other.array

        return other.regroup(
            _einsum(
                # This is a 'matrix' multiplication using the first 2 axis of the left side
                # and the first axis of the right side.
                "ab...,b...->a...",
                self_array,
                other_array,
            )
        )


class Projector(SFXObject):
    """"""

    __slots__ = [
        "basis",
        "trajectory_integral",
        "projection_modifier",
    ]

    def __init__(
        self,
        basis: Basis,
        trajectory_integral: TrajectoryIntegral | TrajectoryIntegralFunc,
        *args,
        projection_modifier: Partial = Partial(lambda projectee: projectee._combine()),
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.basis = basis
        self.trajectory_integral = trajectory_integral
        self.projection_modifier = projection_modifier

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, data: Data, parameters: ParameterGroup):
        return self.basis(data, parameters["basis"])

    @partial(jax.jit, static_argnums=(0,))
    def compute_basis_outer_product(self, basis_values, transformation_values):
        """Computes the outer product of the basis values.

        :param basis_values: The values of the basis at a given spatio-temporal point.

        :return: The outer product of the basis values.
        """

        if transformation_values is not None:
            outer_product = _einsum(
                "ai...m,ijmn,bj...n->iab",
                basis_values,
                transformation_values,
                basis_values,
            )
        else:
            outer_product = _einsum(
                "ai...,bi...->iab",
                basis_values,
                basis_values,
            )
        return outer_product

    @partial(jax.jit, static_argnums=(0,))
    def orthonormalize(
        self,
        orthonormalization_matrix: OrthonormalizationMatrix,
        projections,
    ):
        if isinstance(orthonormalization_matrix, OrthonormalizationMatrix):
            inv_matrix = orthonormalization_matrix.inverse.array
        else:
            inv_matrix = jnp.linalg.pinv(orthonormalization_matrix, hermitian=True)

        return inv_matrix, inv_matrix @ projections

    # @partial(jax.jit, static_argnums=(0,))
    # def _compute_basis_orthonormalization_matrix(self, _, basis_outer_product):
    #     """Computes the orthonormalization_matrix from basis_values.
    #
    #     :param basis_outer_product: The values of the basis at a given spatio-temporal point.
    #
    #     :return: The orthonormalization matrix for the basis values.
    #     """
    #     return (_, jnp.linalg.pinv(basis_outer_product, hermitian=True))
    #
    # @partial(jax.jit, static_argnums=(0,))
    # def orthonormalize(
    #     self,
    #     orthonormalization_matrix: OrthonormalizationMatrix,
    #     coefficients,
    # ):
    #     return jax.tree_util.tree_map(
    #         lambda coeff: self.trajectory_integral.map(
    #             lambda _, matrix, coefficient: matrix.inverse @ coefficient,
    #             orthonormalization_matrix,
    #             coeff,
    #         ),
    #         coefficients,
    #         is_leaf=lambda leaf: isinstance(leaf, DataGroup),
    #     )


class ProjectorGMGS(Projector):
    """"""

    __slots__ = ["orthogonalizer"]

    def __init__(
        self,
        *args,
        orthogonalizer: Optional[Basis] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.orthogonalizer = orthogonalizer

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, data: Data, parameters: ParameterGroup):
        basis = self.basis(data, parameters["basis"])
        if self.orthogonalizer:
            orthogonalizer = self.orthogonalizer(data, parameters["orthogonalizer"])
            orthogonalized_basis = group_iterative_mgs_orthogonalizer(
                basis, orthogonalizer
            )
        else:
            orthogonalized_basis = group_iterative_mgs(basis)
        return basis, orthogonalized_basis

    @partial(jax.jit, static_argnums=(0,))
    def orthonormalize(
        self,
        matrix,
        projection,
        combination=None,
        nbparameters=None,
    ):
        coefficients = jnp.zeros_like(projection)
        out_matrix = jnp.zeros_like(matrix)

        _select = jnp.outer(combination, combination)
        _start = 0

        for nb in nbparameters:
            _end = _start + nb
            _mask = _select[_start:_end, _start:_end]
            _matrix = _mask * matrix[_start:_end, _start:_end]
            out_matrix = out_matrix.at[_start:_end, _start:_end].set(_matrix)
            inv_matrix = jnp.linalg.pinv(_matrix)
            coefficients = coefficients.at[_start:_end].set(
                jnp.matmul(inv_matrix, projection[_start:_end])
            )
            _start += _end

        return out_matrix, coefficients
