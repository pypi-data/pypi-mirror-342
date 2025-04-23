""""""

__all__ = ["Statistics"]

import jax
from jax import lax
import jax.numpy as jnp
import jax.scipy as jsp

from sfx.core.sfx_object import SFXIterable


class Statistics(SFXIterable):
    __slots__ = ["mean", "bias", "error"]

    def __init__(
        self, mean=None, bias=None, error=None, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.mean = mean
        self.bias = bias
        self.error = error
