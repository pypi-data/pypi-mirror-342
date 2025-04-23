""""""

__all__ = [
    "PlotData",
]

import jax
import jax.numpy as jnp

from typing import Any
from functools import partial

from sfx.core.sfx_object import SFXCallable
from sfx.basis.interactions import Interactions
from sfx.basis.parameters import ParameterGroup
from sfx.inference.data import Data
from sfx.utils.console.progress_bar import ProgressBarScan


class PlotData(SFXCallable):
    """Base class for basis"""

    __slots__ = [
        "__dict__",
    ]

    def __init__(self, **kwargs):
        """"""
        super().__init__()
        self.__dict__.update(kwargs)

    # @partial(jax.jit, static_argnums=(0,))
    def __call__(self, data: Data, parameters: ParameterGroup) -> "PlotData":
        if len(data) > 1:
            variables = self._scan_compute_data(data, parameters)
            output = self.regroup(
                [[jnp.moveaxis(g, 0, 1) for g in var] for var in variables]
            )
        else:
            output = self.regroup(self._compute_data(data, parameters))

        return output

    @partial(jax.jit, static_argnums=(0,))
    def _compute_data(self, data: Data, parameters: ParameterGroup) -> Any:
        # _cls = type(self)
        return tuple(
            [
                g.grp
                for g in self.__getattribute__(attr)(
                    data.coordinates, data.time, parameters[i]
                ).grp
            ]
            for i, attr in enumerate(self._getattrs(internal=False))
        )

    @partial(jax.jit, static_argnums=(0,))
    def _scan_compute_data(
        self, data: Data, parameters: ParameterGroup
    ) -> Any:
        @ProgressBarScan(len(data), message="Computing plot data")
        def scan_compute_data(_, x):
            (data,) = x
            return (
                None,
                self._compute_data(data, parameters),
            )

        _, scannee = jax.lax.scan(
            scan_compute_data,
            None,
            (jnp.arange(len(data)), data),
        )
        return scannee

    def regroup(self, groups):
        _cls = type(self)

        return _cls(
            **{
                attr: self.__getattribute__(attr).functions.regroup(
                    [[gg for gg in g] for g in groups[i]]
                )
                for i, attr in enumerate(self._getattrs(internal=False))
            }
        )
