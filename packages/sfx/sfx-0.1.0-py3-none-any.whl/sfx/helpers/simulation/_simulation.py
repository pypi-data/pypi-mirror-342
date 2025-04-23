"""Helpers for simulation runs and results."""

__all__ = [
    "sequential_simulation",
    "combine_simulation_sequences",
]

import os
from typing import Callable

import jax.numpy as jnp
from jax.tree_util import tree_flatten, tree_unflatten

from sfx.core.sfx_object import SFXIterable
from sfx.helpers.io import load, save
from sfx.simulate.core import Simulate, SimulateFunctionParameters


def _append(arg1: SFXIterable, arg2: SFXIterable):
    """Append the second argument to the first argument."""
    tree_arg1, pytree = tree_flatten(arg1)
    tree_arg2, _ = tree_flatten(arg2)

    append_result = tree_unflatten(
        pytree,
        [
            jnp.append(leaf1, leaf2, axis=0)
            for leaf1, leaf2 in zip(tree_arg1, tree_arg2)
        ],
    )

    return append_result


def sequential_simulation(
    simulation: Simulate,
    simfunc_parameters: list[SimulateFunctionParameters],
    lengths: list[int],
    sequences: list[str],
    dir_path: str,
    modifier: Callable = lambda sim, param, seq: None,
    **mkdirkw,
):
    """Performs several simulation runs squentially."""
    os.makedirs(dir_path, **mkdirkw)

    for length, seq, simfunc_param in zip(
        lengths,
        sequences,
        simfunc_parameters,
    ):
        seq_filename = str(dir_path + f"{seq}.h5")
        modifier(simulation, simfunc_param, seq)
        _, states = simulation.integrate(
            length,
            simfunc_param,
        )

        save(states, seq_filename)


def combine_simulation_sequences(
    sequences: list[str],
    dir_path: str,
):
    """Performs several simulation runs squentially."""

    states = None

    dir_path = dir_path + "/" if not dir_path.endswith("/") else dir_path

    for seq in sequences:
        seq_filename = str(dir_path + f"{seq}.h5")

        loaded_states = load(seq_filename)

        if states is None:
            states = loaded_states
        else:
            states = _append(states, loaded_states)

    return states
