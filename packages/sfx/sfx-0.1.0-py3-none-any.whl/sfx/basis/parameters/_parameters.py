""""""

__all__ = ["Parameters", "ParameterGroup"]

from dataclasses import dataclass, fields

from sfx.core.sfx_object import SFXGroup, SFXObject


@dataclass(kw_only=True, repr=False)
class Parameters(SFXObject):
    """Base class for parameters."""

    __slots__ = ["__dict__"]

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    # def __getitem__(self, index):
    #    print(index)
    #    return list(self.__dict__.values())[index]
    #    # type(self)(**{k: v for k, v in list(self.__dict__.items())[index]})


class ParameterGroup(SFXGroup):
    __slots__ = []

    def __init__(self, gid, grp) -> None:
        super().__init__(gid=gid, grp=grp)
