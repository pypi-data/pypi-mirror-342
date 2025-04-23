"""Progress bar compatible with JAX."""

__all__ = ["ProgressBarScan", "ProgressBarForLoop"]

from abc import abstractmethod
from functools import partial, wraps
from typing import Any, Callable, Optional, Tuple

from jax import lax
from jax.experimental import host_callback
from tqdm import tqdm

# from tqdm.auto import tqdm


class ProgressBar(object):
    def __init__(
        self,
        niter: int,
        message: Optional[str] = None,
        tqdm_options: dict = {},
    ) -> None:
        self.niter: int = niter

        if message is None:
            self.message: str = f"Running for {self.niter} iterations"
        else:
            self.message = message

        self.tqdm_options: dict = {
            "ncols": 60,
        } | tqdm_options

    @property
    def update_rate(self) -> int:
        if self.niter > 20:
            update_rate: int = int(self.niter / 20)
        else:
            update_rate = 1
        return update_rate

    @property
    def remainder(self) -> int:
        return self.niter % self.update_rate

    def _define_tqdm(self, arg, transform):
        self.bar = tqdm(range(self.niter), **self.tqdm_options)
        self.bar.set_description(self.message, refresh=False)

    def _update_tqdm(self, arg, transform):
        self.bar.update(arg)

    def _update_progress_bar(self, iteration: int):
        "Updates tqdm progress bar of a JAX scan or loop"
        _ = lax.cond(
            iteration == 0,
            lambda _: host_callback.id_tap(self._define_tqdm, None, result=iteration),
            lambda _: iteration,
            operand=None,
        )

        _ = lax.cond(
            # update tqdm every multiple of `print_rate` except at the end
            (iteration % self.update_rate == 0)
            & (iteration != self.niter - self.remainder),
            lambda _: host_callback.id_tap(
                self._update_tqdm, self.update_rate, result=iteration
            ),
            lambda _: iteration,
            operand=None,
        )

        _ = lax.cond(
            # update tqdm by `remainder`
            iteration == self.niter - self.remainder,
            lambda _: host_callback.id_tap(
                self._update_tqdm, self.remainder, result=iteration
            ),
            lambda _: iteration,
            operand=None,
        )

    def _close_tqdm(self, arg, transform):
        self.bar.close()

    def close_tqdm(self, result, iteration):
        return lax.cond(
            iteration == self.niter - 1,
            lambda _: host_callback.id_tap(self._close_tqdm, None, result=result),
            lambda _: result,
            operand=None,
        )

    @abstractmethod
    def __call__(self, func):
        pass


class ProgressBarForLoop(ProgressBar):
    def __call__(self, func: Callable[[int, Any], Any]):
        """Decorator that adds a progress bar to `body_fun` used in `lax.fori_loop`."""

        @wraps(func)
        def wrapper_progress_bar(i, val):
            self._update_progress_bar(i)
            result = func(i, val)
            return self.close_tqdm(result, i)

        return wrapper_progress_bar


class ProgressBarScan(ProgressBar):
    def __call__(self, func: Callable[[Any, Any], Tuple[Any, Any]]):
        """Decorator that adds a progress bar to `body_fun` used in `lax.scan`."""

        @wraps(func)
        def wrapper_progress_bar(carry, x):
            if type(x) is tuple:
                iter_num = x[0]
                args = x[1:]
                result = func(carry, args)
            else:
                iter_num = x
                result = func(carry, x)

            self._update_progress_bar(iter_num)
            return self.close_tqdm(result, iter_num)

        return wrapper_progress_bar
