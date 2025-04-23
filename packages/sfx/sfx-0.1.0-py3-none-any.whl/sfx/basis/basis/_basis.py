""""""

__all__ = ["Basis", "BasisGradient"]

from functools import partial
from typing import Any, Optional

import jax
from jax.tree_util import Partial

from sfx.basis.interactions import InteractionGradients, Interactions
from sfx.basis.parameters import ParameterGroup, Parameters
from sfx.core.sfx_object import SFXObject
from sfx.inference.data import Data


class Basis(SFXObject):
    """Base class for basis"""

    __slots__ = ["function", "modifier"]

    def __init__(
        self,
        interactions: Interactions,
        modifier: Partial = Partial(lambda x: x),
    ):
        """Initialize the basis with interactions and parameters.

        :param interactions: Interactions function.
        :param parameters: Interaction parameters.
        """

        self.function = interactions
        self.modifier = modifier

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, data: Data, parameters: ParameterGroup) -> Any:
        return self.modifier(self.function(data.coordinates, data.time, parameters))


class BasisGradient(SFXObject):
    """Base class for basis gradient"""

    __slots__ = ["basis", "gradient_options"]

    def __init__(self, basis: Basis, gradient_options: dict):
        """Initialize the basis with interactions and parameters.

        :param interactions: Interactions function.
        :param parameters: Interaction parameters.
        """
        self.basis = basis
        self.gradient_options = gradient_options

    @partial(jax.jit, static_argnums=(0,))
    def __call__(self, data: Data, parameters: ParameterGroup) -> Any:
        return InteractionGradients(self.basis.function, self.gradient_options)(
            data.coordinates, data.time, parameters
        )
