""""""

__all__ = [
    "Data",
    "DataGroup",
    "ParticleGroup",
    "TemporalGroup",
    "DataGroupFunc",
]

from functools import partial
from typing import Callable

"""Data container for inference."""

import jax
import jax.numpy as jnp

from sfx.core.sfx_object import SFXGroup, SFXIterable, SFXCallable
from sfx.helpers.format import expand_dimensions
from sfx.utils.console.progress_bar import ProgressBarScan


class Data(SFXIterable):
    __slots__ = [
        "frame",
        "time",
        "timestep",
        "coordinates",
        "future_motions",
        "past_motions",
        "coordinates_stratonovitch",
        "velocities",
        "nbparticles",
    ]

    def __init__(
        self,
        *,
        frame,
        time,
        timestep,
        coordinates,
        future_motions,
        past_motions,
        coordinates_stratonovitch,
        velocities,
        nbparticles,
    ) -> None:
        if hasattr(coordinates, "nbdimensions"):
            if coordinates.nbdimensions == 3:
                super().__init__(coordinates.dimensions[0])
            else:
                super().__init__()

        self.frame = frame
        self.time = time
        self.timestep = timestep
        self.coordinates = coordinates
        self.future_motions = future_motions
        self.past_motions = past_motions
        self.coordinates_stratonovitch = coordinates_stratonovitch
        self.velocities = velocities
        self.nbparticles = nbparticles

    @property
    def trajectory_length(self):
        return jnp.sum(self.timestep * self.nbparticles)

    @property
    def time_length(self):
        return jnp.sum(self.timestep)


class DataGroup(SFXGroup):
    __slots__ = []

    def __init__(self, gid, grp) -> None:
        super().__init__(gid=gid, grp=grp)

    @partial(jax.jit, static_argnames=("axes",))
    def _group(self, indices, data, axes=(0,)):
        condition = expand_dimensions(indices, data, axes=axes)
        return jnp.where(condition, data, jnp.nan)

    @partial(jax.jit, static_argnames=("axes",))
    def _group_integrand(self, grp, measures, data, axes):
        return self._group(grp, data, axes=axes) * expand_dimensions(
            measures, data, axes=axes
        )

    @partial(jax.jit, static_argnames=("axes",))
    def _group_weight(self, grp, weights, data, axes):
        return self._group_integrand(grp, weights, data, axes) / jnp.sum(
            jnp.where(grp, weights, 0)
        )

    @partial(jax.jit, static_argnames=("axes",))
    def average(self, weights, data, axes=(0,)):
        cls = type(self)

        averages = jnp.nansum(
            jax.vmap(self._group_weight, in_axes=(0, None, None, None))(
                self.array, weights, data, axes
            ),
            # jax.lax.map(
            #     jax.tree_util.Partial(
            #         self._group_integrand,
            #         weights=weights,
            #         data=data,
            #         axes=axes,
            #     ),
            #     self.array,
            # ),
            axis=tuple([axis + 1 for axis in axes]),
        )

        return cls(self.gid, averages)

    @partial(jax.jit, static_argnames=("axes",))
    def integrate(self, measures, data, axes=(0,)):
        # cls is DataGroup
        cls = type(self)

        integrations = jnp.nansum(
            jax.vmap(self._group_integrand, in_axes=(0, None, None, None))(
                self.array, measures, data, axes
            ),
            # jax.lax.map(
            #     jax.tree_util.Partial(
            #         self._group_integrand,
            #         measures=measures,
            #         data=data,
            #         axes=axes,
            #     ),
            #     self.array,
            # ),
            axis=tuple([axis + 1 for axis in axes]),
        )

        return cls(self.gid, integrations)

    @partial(jax.jit, static_argnums=(1,), static_argnames=("message",))
    def integrate_func(self, func, measures, args, kwargs, message=""):
        # cls is DataGroup
        cls = type(self)

        def _scan_func(carry, xs):
            measures, grp = xs[-2:]
            args = xs[:-2]
            output, kwargs = carry

            new_output = jax.tree_util.tree_map(
                lambda x, y: x + measures * jnp.einsum("g,...->g...", grp, y),
                output,
                func(*args, **kwargs),
                is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
            )

            return ((new_output, kwargs), None)

        init_args = jax.tree_util.tree_map(
            lambda x: x[0],
            args,
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

        init = (
            jax.tree_util.tree_map(
                lambda x: jnp.einsum("g,...->g...", self.array[:, 0], x),
                func(*init_args, **kwargs),
                is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
            ),
            kwargs,
        )

        scan_args = jax.tree_util.tree_map(
            lambda x: x[1:],
            (*args, measures, self.array.T),
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )

        if len(message):
            _length = measures.shape[0] - 1
            _progress_bar = ProgressBarScan(
                _length,
                message=message,
                tqdm_options={"leave": True, "ncols": 80},
            )
            scan_func = _progress_bar(_scan_func)
            scan_args = (jnp.arange(_length), *scan_args)
        else:
            scan_func = _scan_func

        integrated = jax.lax.scan(scan_func, init, scan_args)[0][0]

        # return cls(self.gid, integrated)
        return jax.tree_util.tree_map(
            lambda int: cls(self.gid, int),
            integrated,
            is_leaf=lambda leaf: not isinstance(leaf, (tuple, list)),
        )


class TemporalGroup(DataGroup):
    """Temporal Group"""

    __slots__ = []


class ParticleGroup(DataGroup):
    """Particle Group"""

    __slots__ = []


class DataGroupFunc(SFXCallable):
    __slots__ = ["datagroup", "funcgroup"]

    def __init__(self, datagroup: DataGroup, funcgroup: Callable) -> None:
        super().__init__()
        self.datagroup = datagroup
        self.funcgroup = funcgroup

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, *args, **kwargs):
        super().__call__()
        return self.funcgroup(*args, **kwargs)

    def regroup(self, groups, *args, **kwargs):
        return self.datagroup._regroup_groups(groups, *args, **kwargs)

    def map(
        self,
        func,
        *groups,
        is_leaf=lambda node: not isinstance(node, (DataGroup, list)),
        **kwargs,
    ):
        return jax.tree_util.tree_map(
            lambda *args: func(*args, **kwargs),
            self.datagroup,
            *groups,
            is_leaf=is_leaf,
        )
