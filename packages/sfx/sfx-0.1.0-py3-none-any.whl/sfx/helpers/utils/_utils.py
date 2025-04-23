"""Helpers for general utilies."""

__all__ = [
    "flatten_iterable",
    "flatten_dict",
]

from typing import Dict, Iterable, MutableMapping

from jax import Array


def flatten_iterable(xs: Iterable, cond=lambda _: True):
    """https://stackoverflow.com/a/2158532"""
    for x in xs:
        if cond(x) and (
            isinstance(x, Iterable) and not isinstance(x, (str, bytes, Array))
        ):
            yield from flatten_iterable(x, cond=cond)
        else:
            yield x


def flatten_dict(dictionary: Dict, parent_key: str = "", separator="_"):
    """https://stackoverflow.com/a/6027615"""
    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + str(key) if parent_key else key

        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, separator).items())

        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten_dict({str(k): v}, new_key).items())

        else:
            items.append((new_key, value))
    return dict(items)
