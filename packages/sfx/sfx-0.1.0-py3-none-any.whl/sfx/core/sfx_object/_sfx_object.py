__all__ = ["SFXObject", "SFXIterable", "SFXCallable", "SFXGroup"]

import inspect
import pprint
from itertools import chain
from numbers import Number
from typing import Any, Callable, Generator, List, Tuple, TypedDict

import hickle as hkl
import jax
import jax.numpy as jnp
import numpy as np
from h5py import AttributeManager, Group
from hickle.helpers import PyContainer
from hickle.lookup import LoaderManager
from jax import Array
from jax.tree_util import (
    Partial,
    register_pytree_node_class,
    register_pytree_with_keys_class,
    tree_flatten,
    tree_flatten_with_path,
    tree_leaves,
    tree_leaves_with_path,
    tree_unflatten,
)

from sfx.helpers.math import create_kronecker_delta

CreateGroupOutput = Tuple[Group, Generator[Tuple[Any, Any, dict, dict], None, None]]


class SFXPrettyPrinter(pprint.PrettyPrinter):
    _dispatch = pprint.PrettyPrinter._dispatch.copy()

    def _pprint_sfxobject_(
        self, instance, object, stream, _, allowance, context, level
    ):
        stream.write(f"{object.__class__.__name__}(")
        for s in object._getattrs(internal=False):
            stream.write(f"\n{' ' * level * 2}{s} = ")
            instance._format(
                object.__getattribute__(s),
                stream,
                2 * level,
                allowance + 1,
                context,
                level,
            )
            stream.write(";")
        stream.write(f"\n{' ' * level * 2})")

    def _pprint_sfxgroup_(self, instance, object, stream, _, allowance, context, level):
        stream.write(f"{object.__class__.__name__}(")
        for i, name in enumerate(object.name):
            stream.write(f"\n{' ' * level * 2}{name} = ")
            instance._format(
                object.grp[i],
                stream,
                2 * level,
                allowance + 1,
                context,
                level,
            )
            stream.write(",")
        stream.write(f"\n{' ' * level * 2})")

    def _pprint_(self, instance, object, stream, _, allowance, context, level):
        if isinstance(object, SFXGroup):
            self._pprint_sfxgroup_(
                instance, object, stream, _, allowance, context, level
            )
        else:
            self._pprint_sfxobject_(
                instance, object, stream, _, allowance, context, level
            )

    def update_dispatch(self, cls):
        self._dispatch[cls.__repr__] = self._pprint_

    # @staticmethod
    # def _pprint_partial_(
    #     instance, object, stream, _, allowance, context, level
    # ):
    #     signature = inspect.signature(object.func)
    #     stream.write(f"{object.func.__name__}(")
    #     for p in signature.parameters.values():
    #         stream.write(f"\n{' ' * level * 2}{p.name},")
    #     stream.write(f"\n{' ' * level * 2})")
    #
    # _dispatch[Partial.__repr__] = _pprint_partial_


_SFXPrettyPrinter = SFXPrettyPrinter(indent=2, compact=True, width=80, sort_dicts=True)


def _dump_function(
    py_obj: Any, h_group: Group, name: str, **kwargs: TypedDict
) -> CreateGroupOutput:
    """Dump a class into a hdf5 file with ``hickle``.

    :param py_obj: The instance of the class to be dumped.
    :param h_group: The h5py.Group ``py_obj`` should be dumped into.
    :param name: The name of the ``h5py.Dataset`` or ``h5py.Group``
    representing ``py_obj``.
    :param **kwargs: The compression keyword arguments passed to
    ``hickle.dump``.

    :return: tuple containing h5py.Dataset and empty list of subitems

    """
    ds = h_group.create_group(name)

    if hasattr(py_obj, "__gethstate__"):
        state = py_obj.__gethstate__()

    elif hasattr(py_obj, "__getstate__"):
        state = py_obj.__getstate__()

    else:
        # Temporary as hickle as trouble with jax.Array yet.
        items = []

        for attr in py_obj._getslots():
            value = py_obj.__getattribute__(attr)

            if isinstance(value, jax.Array):
                value = np.asarray(value)

            elif isinstance(value, dict):
                value = {
                    k: (np.asarray(v) if isinstance(v, jax.Array) else v)
                    for k, v in value.items()
                }

            items.append((attr, value, {}, kwargs))

        items = tuple(items)

        # Original version
        # items = tuple(
        #    (attr, py_obj.__getattribute__(attr), {}, kwargs)
        #    for attr in py_obj._getattrs()
        # )

    return ds, items


class _LoadContainer(PyContainer):
    def __init__(self, h5_attrs: dict, base_type: str, object_type: Any) -> None:
        """The load container to recover data dumped by ``hickle``.

        :param    h5_attrs: The attributes dictionary attached to the
        group representing the custom class.
        :param   base_type: Byte string naming the loader to be used for
        restoring the custom class object
        :param py_obj_type: Custom class (or subclass)

        """
        # the optional protected _content parameter of the PyContainer
        # __init__ method can be used to change the data structure used to
        # store the subitems passed to the append method of the PyContainer
        # class per default it is set to []
        super().__init__(h5_attrs, base_type, object_type, _content=dict())

    def append(self, name: str, item: Any, h5_attrs: AttributeManager) -> None:
        """Add a particular item to the content defining the object.

        :param name: Identifies the subitem within the parent ``hdf5.Group``.
        :param item: The object representing the subitem ``h5_attrs``.
        :param h5_attrs: Attributes attached to the ``h5py.Dataset`` or
        ``h5py.Group`` representing the item.

        """

        self._content[name] = item

    def convert(self) -> None:
        """Convert the content read from file to the object itself."""
        # py_obj_type should point to MyClass or any of its subclasses
        NewInstance = self.object_type.__new__(self.object_type)

        if hasattr(NewInstance, "__sethstate__"):
            NewInstance.__sethstate__(self._content)
        elif hasattr(NewInstance, "__setstate__"):
            NewInstance.__setstate__(self._content)
        else:
            for attr in NewInstance._getslots():
                # Temporary as hickle as trouble with jax.Array yet.
                value = self._content[attr]

                if isinstance(value, np.ndarray):
                    value = jnp.asarray(value)

                elif isinstance(value, dict):
                    value = {
                        k: (jnp.asarray(v) if isinstance(v, np.ndarray) else v)
                        for k, v in value.items()
                    }
                else:
                    pass

                NewInstance.__setattr__(attr, value)

                # Original version
                # NewInstance.__setattr__(attr, self._content[attr])
            # if hasattr(NewInstance, "__slots__") and hasattr(NewInstance, "__dict__"):
            #     for s in NewInstance._getslots():
            #         NewInstance.__setattr__(s, self._content[s])
            #     # Update the __dict__ using attributes not found in slots.
            #     NewInstance.__dict__.update({
            #         k:v for k,v in self._content.items()
            #         if k not in NewInstance._getslots()
            #     })
            #
            # elif hasattr(NewInstance, "__slots__"):
            #     for s in NewInstance._getslots():
            #         NewInstance.__setattr__(s, self._content[s])

        if hasattr(NewInstance, "__attrs_post_init__"):
            NewInstance.__attrs_post_init__()

        return NewInstance


class Hicklable(object):
    """Base Class to make all subclass registered by hickle with save and load
    functionalities.
    """

    __slots__ = []

    def __init_subclass__(cls) -> None:
        """Register the subclasses with hickle."""
        LoaderManager.register_class(
            cls,
            f"{cls.__name__}".encode(encoding="utf-8"),
            dump_function=_dump_function,
            container_class=_LoadContainer,
        )

    def save(self, output: str = "default.h5") -> None:
        """Dump the class to a hdf5 file using ``hickle.dump``.

        :param output: Name of the file to dump the class to.

        """
        hkl.dump(self, output)

    def load(self, input: str = "default.h5") -> None:
        """Load a class from a hdf5 file created by ``hickle``.

        :param input: Name of the file to load from.

        """

        NewInstance = hkl.load(input)

        if self.__class__ == NewInstance.__class__:
            for attr in NewInstance._getslots():
                self.__setattr__(attr, NewInstance.__getattribute__(attr))
            # if hasattr(NewInstance, "__slots__") and hasattr(NewInstance, "__dict__"):
            #     for s in NewInstance._getslots():
            #         self.__setattr__(s, NewInstance.__getattribute__(s))
            #     self.__dict__.update(NewInstance.__dict__)
            #
            # elif hasattr(self, "__slots__") :
            #     for s in self._getslots() :
            #         self.__setattr__(s, NewInstance.__getattribute__(s))
        else:
            raise TypeError(
                "Trying to load a different class: "
                f"{self.__class__} != {NewInstance.__class__}."
                "Operation Aborted."
            )

    @classmethod
    def _getslots(cls, internal=True):
        """Returns slots from the current class and its parents in heritance order."""
        if hasattr(cls, "__slots__"):
            slots = (
                slot
                for parent in cls.__mro__[::-1][1:]
                for slot in parent.__slots__
                if (not slot.startswith("_")) or internal
            )
        else:
            # Empty generator
            slots = zip()
        return slots

    def _getdicts(self, internal=True):
        """Returns dicts from the current class and its parents in heritance order."""
        if hasattr(self, "__dict__"):
            keys = (
                key
                for key in self.__dict__.keys()
                if (not key.startswith("_")) or internal
            )
        else:
            # Empty generator
            keys = zip()
        return keys

    def _getattrs(self, internal=True):
        """Returns attributes from the current class and its parents in heritance order."""
        return chain(*[self._getslots(internal), self._getdicts(internal)])


class SFXObject(Hicklable):
    """Base class for SFX."""

    __slots__ = []

    def __init_subclass__(cls) -> None:
        """Register the subclasses with JAX."""
        register_pytree_with_keys_class(cls)
        # register_pytree_node_class(cls)
        _SFXPrettyPrinter.update_dispatch(cls)

    def __repr__(self, _jax_compatible=False):
        clsname = self.__class__.__name__
        clsparams = ",".join(
            [
                f"{attr}={self.__getattribute__(attr)}"
                for attr in self._getattrs(internal=False)
            ]
        )

        return f"{clsname}({clsparams})"

    def __str__(self):
        return _SFXPrettyPrinter.pformat(self)

    # def __hash__(self) -> int:
    #     return hash(self.__repr__())

    def tree_flatten_with_keys(self):
        aux_data = tuple(self._getattrs(internal=False))
        children_with_keys = tuple(
            (attr, self.__getattribute__(attr)) for attr in aux_data
        )
        return (children_with_keys, aux_data)

    def tree_flatten(self):
        aux_data = tuple(self._getattrs(internal=False))
        children = tuple(self.__getattribute__(k) for k in aux_data)
        # if hasattr(self, "__slots__") and hasattr(self, "__dict__"):
        #    aux_data = tuple(list(self._getslots()) + list(self.__dict__.keys()))
        #    children = tuple(self.__getattribute__(k) for k in aux_data)

        # elif hasattr(self, "__slots__") :
        #    aux_data = tuple(self._getslots())
        #    children = tuple(self.__getattribute__(slot) for slot in aux_data)

        return (children, aux_data)

    @classmethod
    def tree_unflatten(cls, aux_data, children):
        return cls(**{f"{s}": v for s, v in zip(aux_data, children)})


class SFXCallable(SFXObject):
    """Base class for callable SFX objects."""

    __slots__ = ["_called"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._called = 0

    def __bool__(self):
        return self._called > 0

    def __call__(self):
        self._called += 1

    # def __hash__(self) -> int:
    #     return super().__hash__()
    def __getitem__(self, index):
        cls = type(self)

        if isinstance(index, str):
            item = self.__getitem_str_(index)

        elif isinstance(index, int):
            item = self.__getitem_int_(index)

        else:
            raise TypeError(f"{cls.__name__} indices must be integer or string.")

        return item

    def __getitem_str_(self, string: str):
        return self.__getattribute__(string)

    def __getitem_int_(self, index: int):
        _attr = next(
            attr for i, attr in enumerate(self._getattrs(internal=False)) if i == index
        )
        return self.__getattribute__(_attr)


class SFXIterable(SFXObject):
    __slots__ = [
        "_current_index",
        "_length",
    ]

    def __init__(self, _length=1) -> None:
        super().__init__()
        self._length = _length
        self._current_index = 0

    def __hash__(self) -> int:
        return hash(self.__repr__(_jax_compatible=True))

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length: int):
        if not isinstance(length, int) or length <= 0:
            raise ValueError(f"length must be > 0; got {length}")
        self._length = length

    def __iter__(self):
        return self

    def __len__(self):
        return self._length

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._getattrs(internal=False)

        elif isinstance(item, type(self)):
            return item in (o for o in self)
        else:
            raise TypeError(
                f"Left-hand object for `in` operator should be "
                f"{type(self).__name__} or str; got {type(item).__name__}"
            )

    def __eq__(self, other):
        cls = type(self)
        assert isinstance(
            other, type(self)
        ), f"Right-hand side should be a {cls.__name__}, not {type(other).__name__}"

        self_leaves = tree_leaves(self)
        other_leaves = tree_leaves(other)

        are_equal = True
        for s, o in zip(self_leaves, other_leaves):
            if isinstance(s, Array) and isinstance(o, Array):
                if s.shape == o.shape:
                    if not jnp.all(s == o):
                        are_equal = False
                        break
                else:
                    are_equal = False
                    break

            elif not s == o:
                are_equal = False
                break

        return are_equal

    def __next__(self):
        if self._length > 1:
            if self._current_index < self._length:
                flattened, tree = tree_flatten(self)

                state = tree_unflatten(
                    tree, (flat[self._current_index] for flat in flattened)
                )
                self._current_index += 1
                return state
            else:
                self._current_index = 0

            raise StopIteration
        else:
            return self

    def __getitem_str_(self, string: str):
        if string in self._getattrs(internal=False):
            return self.__getattribute__(string)
        else:
            raise KeyError(f"No such attribute: {string}")

    def __getitem_int_(self, index: int):
        flattened, tree = tree_flatten(self)

        if index < len(self):
            # If we have only one state, we return it
            # 17/04/2024 is it really wanted? !!! IF BUG OCCURS CHECK HERE !!!
            # if len(self) == 1:
            #     item = self
            #
            # else:
            # If the flattened PyTree has dimensions (ndim>0) we select it
            # based on the index. Else we just return the value.
            item = tree_unflatten(
                tree,
                (
                    flat[index] if hasattr(flat, "ndim") and flat.ndim else flat
                    for flat in flattened
                ),
            )

            return item

        else:
            raise IndexError(
                f"Index out of range; got {index} while length is {len(self)}"
            )

    def __getitem_slice_(self, slc: slice):
        flattened, tree = tree_flatten(self)

        if len(self) == 1:
            # When there is only one element, we check that the slice
            # contains that element and return it.
            # Otherwise we return an empty element
            if (
                slc.start is None
                or slc.start < len(self)
                and (slc.stop is None or slc.stop > len(self))
                and (slc.step is None or slc.step % 2 == 0)
            ):
                item = self
            else:
                item = self.__init__()
        else:
            item = tree_unflatten(tree, (flat[slc] for flat in flattened))

        return item

    def __getitem_list_(self, index: list | Array):
        flattened, tree = tree_flatten(self)

        if len(index) < len(self):
            # If we have only one state, we return it
            if len(self) == 1:
                item = self

            else:
                # If the flattened PyTree has dimensions (ndim>0) we select it
                # based on the index. Else we just return the value.
                item = tree_unflatten(
                    tree,
                    (
                        (
                            jnp.stack([flat[i] for i in index], axis=0)
                            if hasattr(flat, "ndim") and flat.ndim
                            else flat
                        )
                        for flat in flattened
                    ),
                )

            return item

        else:
            raise IndexError(
                f"Index out of range; got {index} while length is {len(self)}"
            )

    def __getitem__(self, index):
        cls = type(self)

        if isinstance(index, str):
            item = self.__getitem_str_(index)

        elif isinstance(index, slice):
            item = self.__getitem_slice_(index)

        elif isinstance(index, (list, Array)):
            item = self.__getitem_list_(index)

        elif isinstance(index, int) or any(
            map(lambda x: x == index.dtype, (jnp.int32, jnp.int64))
        ):
            item = self.__getitem_int_(index)

        else:
            raise TypeError(
                f"{cls.__name__} indices must be integers, slices or strings; got {type(index)}"
            )

        return item

    def __iadd__(self, other):
        cls = type(self)

        assert isinstance(
            other, type(self)
        ), f"Right-hand side should be a {cls.__name__}, not {type(other).__name__}"

        self_leaves, self_tree = tree_flatten(self)
        other_leaves = tree_leaves(other)

        # This is a bit hacky yet
        if len(self) == 1 and len(other) == 1:
            # _do_add = []

            # We skip CustomNode PyTrees if the (number of nodes) != (number of leaves)
            # for c in self_tree.children():
            #     _do_add.append(True)
            #     if c.num_nodes == c.num_leaves:
            #        _do_add.append(True)
            #     else:
            #        _do_add.extend(c.num_leaves * [False])

            # for i, (sl, ol, _da) in enumerate(zip(self_leaves, other_leaves, _do_add)):
            for i, (sl, ol) in enumerate(zip(self_leaves, other_leaves)):
                # When there is only one element for each, we just update
                # arrays.
                # If it has more than one leaf then it we skip it
                # if _da and (isinstance(sl, Array) and isinstance(ol, Array)):
                if isinstance(sl, Array) and isinstance(ol, Array):
                    if all(
                        sl.shape[axis] == ol.shape[axis] for axis in range(1, sl.ndim)
                    ):
                        self_leaves[i] = jnp.append(sl, ol, axis=0)
                    else:
                        raise TypeError(
                            "Trying to add element that have different shapes "
                            "outside the concatenation axis (0): "
                            "{sl.shape[1:]} != {ol.shape[1:]}"
                        )
        else:
            for i, (sl, ol) in enumerate(zip(self_leaves, other_leaves)):
                # When self or other contains more than one element we
                # append it.
                if not isinstance(sl, Array):
                    sl = jnp.asarray(sl)[jnp.newaxis]

                if not isinstance(ol, Array):
                    o = jnp.asarray(ol)[jnp.newaxis]

                if sl.ndim < ol.ndim:
                    sl = sl[jnp.newaxis]

                elif sl.ndim > ol.ndim:
                    ol = ol[jnp.newaxis]

                if all(sl.shape[axis] == ol.shape[axis] for axis in range(1, sl.ndim)):
                    self_leaves[i] = jnp.append(sl, ol, axis=0)
                else:
                    raise TypeError(
                        "Trying to add element that have different shapes "
                        "outside the concatenation axis (0): "
                        "{sl.shape[1:]} != {ol.shape[1:]}"
                    )

        return tree_unflatten(self_tree, self_leaves)

    def __add__(self, other):
        cls = type(self)

        assert isinstance(
            other, type(self)
        ), f"Left- and right-side should be of the same type. Not {cls.__name__} + {type(other).__name__}"
        # Temporary object of type cls that will contain the result of the
        # addition
        _temp = cls(
            **{
                attr: self.__getattribute__(attr)
                for attr in self._getattrs(internal=False)
            }
        )
        _temp += other

        return _temp


class SFXGroup(SFXIterable):
    __slots__ = ["gid", "grp", "_is_numeric"]

    def __hash__(self):
        return super().__hash__()

    def __init__(self, gid, grp) -> None:
        self.gid = gid
        self.grp = grp

        # print(self.gid)
        if hasattr(gid, "__len__"):
            # if isinstance(gid, jax.Array):
            #     gid = (
            #         list(map(lambda g: self._decode_gid(g).strip(" "), gid))
            #         if (isinstance(gid, jax.Array) and gid.ndim > 1)
            #         else self._decode_gid(gid.strip(" "))
            #     )
            #
            if isinstance(gid, list):
                # _max_length = max(map(lambda x: len(x), gid))
                # self.gid = jnp.asarray(
                #     list(
                #         map(
                #             self._encode_gid,
                #             map(lambda x: x + " " * (_max_length - len(x)), gid),
                #         )
                #     )
                # )
                self.gid = gid

                if isinstance(grp, (jax.Array, list, tuple, type(self))):
                    assert len(gid) == len(
                        grp
                    ), f"The number of names ({len(gid)}) should match the number of groups ({len(grp)})."

            super().__init__(len(gid))

        self._is_numeric = self._check_numeric(grp)

    @property
    def group(self):
        """Returns the groups as a multi-dimensional list"""
        return self._restructure(self._get_group(self.grp))

    @property
    def array(self):
        """Returns the groups as a homogeneous array"""
        if self._is_numeric:
            groups = jnp.asarray(
                [grp.array if isinstance(grp, SFXGroup) else grp for grp in self]
            )
            # jnp.stack(self._homogenize(self._get_group(self.grp)))
            # .reshape(
            #     *self._get_shape_numeric(self, self.tree)
            # )
        else:
            raise RuntimeError(
                "Group does not contain numerical data and cannot be homogenized as an array."
            )

        return groups

    def _get_group(self, groups, group_array=None):
        if group_array is None:
            group_array = []

        for grp in groups:
            if isinstance(grp, SFXGroup):
                new_group = self._get_group(grp.grp, group_array=[])
                group_array.extend(new_group)

            elif isinstance(grp, (list, tuple)):
                new_group = self._get_group(grp, group_array=[])

                group_array.extend(new_group)

            else:
                group_array.append(grp)

        return group_array

    def _restructure(
        self,
        groups,
        _restructured_groups=None,
        _tree=None,
        _count=None,
        _depth=None,
    ):
        if _restructured_groups is None:
            _restructured_groups = []
            _tree = self.tree
            _count = [0]
            _depth = [0]

        if not _count[0] == len(groups):
            if _tree[1] is not None:
                for _t in _tree[1]:
                    _old_count = _count[0]
                    _restructured_groups.append(
                        self._restructure(
                            groups,
                            _restructured_groups=[],
                            _tree=_t,
                            _count=_count,
                            _depth=[_depth[0] + 1],
                        )
                    )

            else:
                _slice = slice(_count[0], _count[0] + _tree[0])

                if self.is_numeric:
                    print("count:", _count[0])
                    _restructured_groups = jnp.stack(groups[_slice])
                    # print(groups, _slice, groups[_slice], sep="\n")
                else:
                    _restructured_groups.extend(groups[_slice])
                _count[0] = _slice.stop

        return _restructured_groups

    def _homogenize(self, groups):
        """Homogenize the arrays such that they can be combined in a same array."""

        homogenized_groups = []

        # List all the shapes in groups and find the m
        shapes = list(map(lambda g: g.shape, groups))
        max_index = max(enumerate(shapes), key=lambda x: x[1])[0]
        max_shape = shapes[max_index]

        for _, (group, shape) in enumerate(zip(groups, shapes)):
            if len(shape) < len(max_shape):
                broadcasted_group = jnp.broadcast_to(group, max_shape)
                index = len(max_shape) - len(shape)
                # next(find_conv(jnp.asarray(max_shape), jnp.asarray(shape)))

                kronecker_delta = create_kronecker_delta(*max_shape[: index + 1])
                # if the element of the group to be broadcasted has shape
                if group[tuple(0 for _ in range(index))].shape:
                    kronecker_delta = jnp.expand_dims(
                        kronecker_delta,
                        axis=index + 1,
                    )

                # The delta kronecker tensor makes sure that no values are duplicated but only
                # "moved" around
                homogenized_groups.append(broadcasted_group * kronecker_delta)
            else:
                homogenized_groups.append(group)

        return homogenized_groups

    @property
    def is_numeric(self):
        if self._is_numeric is None:
            self._is_numeric = self._check_numeric(self.grp)
        return self._is_numeric

    @property
    def shape(self):
        """Returns a homogeneous array shape when possible else a tree shape."""

        if self.is_numeric:
            shape = self.array.shape
        else:
            shape = self.tree

        return shape

    # def _get_shape_numeric(self, grp, tree, _shape=None):
    #     if _shape is None:
    #         _shape = []
    #
    #     _length, _leaf = tree
    #     if all(a == b for a in _leaf for b in _leaf):
    #         _shape.append(_length)
    #         self._get_shape_numeric(grp[0], _leaf[0], _shape=_shape)
    #
    #     else:
    #         _shape.extend(grp.shape)
    #
    #     return _shape

    def _check_numeric(self, groups, is_numeric=True):
        if is_numeric:
            if isinstance(groups, SFXGroup):
                for grp in groups.grp:
                    is_numeric = self._check_numeric(grp, is_numeric=is_numeric)

            elif isinstance(groups, (list, tuple)):
                for grp in groups:
                    is_numeric = self._check_numeric(grp, is_numeric=is_numeric)

            elif not isinstance(groups, (jax.Array, Number)):
                return False

            else:
                # This condition means we reached a jax.Array or Number
                return True

        return is_numeric

    def _init_from_group(self, other: "SFXGroup") -> None:
        assert isinstance(
            other, SFXGroup
        ), f"Intialisation from group requires another SFXGroup; Got {type(other)}"

        # Loops over the external attributes of other and assign them
        # to the current SFXGroup
        for attr in other._getattrs(internal=False):
            self.__setattr__(attr, other.__getattribute__(attr))

    @property
    def name(self):
        return self.gid
        # (
        #     list(map(lambda g: self._decode_gid(g).strip(" "), self.gid))
        #     if (isinstance(self.gid, jax.Array) and self.gid.ndim > 1)
        #     else self._decode_gid(self.gid.strip(" "))
        # )

    @property
    def tree(self):
        """
        Returns a representations of the group as a an arboresence
        tree.

        Each node contains the number of nodes/leaves at index 0
        and the sub-tree (nodes) at index 1. After an index of 1
        the (nodes) are indexable.
        """
        tree = self._get_nodes(self.grp)
        return tree

    def _get_nodes(self, groups, nodes=None):
        """
        Get the nodes for the tree representation for the group.
        """
        if nodes is None:
            nodes = []

        if isinstance(groups, SFXGroup):
            nodes.append(len(groups))
            _tmp = []
            for grp in groups.grp:
                node = self._get_nodes(grp, nodes=[])
                if node is not None:
                    _tmp.append(node)
                else:
                    _tmp = None
                    break

            nodes.append(_tmp)
            # nodes.append(
            #    [self._get_nodes(grp, nodes=[]) for grp in groups.grp]
            # )
            # nodes.append(
            #     [self._get_nodes(grp, nodes=[]) for grp in groups.grp]
            # )

        elif isinstance(groups, (list, tuple)):
            nodes.append(len(groups))
            _tmp = []
            for grp in groups:
                node = self._get_nodes(grp, nodes=[])
                if node is not None:
                    _tmp.append(node)
                else:
                    _tmp = None
                    break

            nodes.append(_tmp)
            # nodes.append(len(groups))
            # nodes.append([self._get_nodes(grp, nodes=[]) for grp in groups])

        elif isinstance(groups, Array):
            shape = groups.shape

            # If the array has no shape, then it is a scalar such that
            # the length = 0
            nodes = self._shape_to_tree(shape)

        return nodes

    def _shape_to_tree(self, shape, tree=None):
        if tree is None:
            tree = []

        if shape:
            tree.append(shape[0])
            _tmp = []

            for _ in range(shape[0]):
                node = self._shape_to_tree(shape[1:])

                if node is not None:
                    _tmp.append(node)
                else:
                    _tmp = None
                    break

            tree.append(_tmp)
        else:
            tree = None
        return tree

    def _encode_gid(self, input_gid):
        """Created a unique unsigned int identifier for a string.
        It allows strings to be vmapped.
        """
        if isinstance(input_gid, str):
            gid = jnp.asarray(
                list(map(ord, input_gid)),
                dtype=jnp.uint16,
            )

        else:
            gid = input_gid

        return gid

    def _decode_gid(self, input_gid):
        if isinstance(input_gid, (jax.Array, list, tuple)):
            gid = bytes(list(input_gid)).decode()
        else:
            gid = input_gid

        return gid

    def regroup(self, groups, gid=None):
        cls = type(self)

        # This doesn't work well with scan as the this first dimension will not match the
        # group
        if gid is None:
            gid = self.gid
            if isinstance(groups, jax.Array):
                new_groups = self._regroup_array(groups)
            else:
                new_groups = self._regroup_groups(groups)
        else:
            new_groups = groups

        return cls(gid=gid, grp=new_groups)

    def _regroup_groups(self, groups):
        cls = type(self)
        new_groups = []

        for i, _ in enumerate(self.gid):
            current_grp = self.grp[i]
            grp = groups[i]

            # If a sub-group is a group of the same type, then we restore the gid and sub-group
            # unless there's a mismatch between the initial sub-group and the new sub-group
            if isinstance(current_grp, SFXGroup) and len(current_grp) == len(grp):
                if all(isinstance(grp, SFXGroup) for grp in current_grp.grp):
                    # Changed on 07/06/2024
                    # new_groups.append(current_grp.regroup(grp))
                    new_groups.append(current_grp._regroup_groups(grp))
                else:
                    new_groups.append(type(self.grp[i])(gid=self.grp[i].gid, grp=grp))
            else:
                new_groups.append(grp)
        return cls(gid=self.gid, grp=new_groups)

    def _regroup_array(self, array):
        cls = type(self)
        new_groups = []

        # index = slice(None, None, None)
        # if len(self.gid) == len(array):
        #     index = 0

        offset = 0

        for i, _ in enumerate(self.gid):
            current_grp = self.grp[i]
            if isinstance(current_grp, jax.Array):
                if current_grp.shape:
                    grp_length = current_grp.shape[0]
                else:
                    grp_length = 1
            else:
                grp_length = len(current_grp)

            index = slice(None, None, None)
            if grp_length == 1:
                index = 0

            grp = array[offset : offset + grp_length]
            offset += grp_length

            if isinstance(current_grp, SFXGroup) and len(current_grp) == len(grp):
                if all(isinstance(grp, SFXGroup) for grp in current_grp.grp):
                    new_groups.append(current_grp._regroup_array(grp[index]))
                else:
                    new_groups.append(type(self.grp[i])(gid=self.grp[i].gid, grp=grp))
            elif isinstance(current_grp, SFXGroup):
                new_groups.append(current_grp._regroup_array(grp[index]))
            else:
                new_groups.append(grp[index])

        return cls(gid=self.gid, grp=new_groups)

    def sum(self, axis=0):
        if not self.is_numeric:
            raise RuntimeError(
                "Trying to sum over axis for an instance that does not contain numerical data; "
                f"Instance is:\n{self.__repr__(_jax_compatible=True)}"
            )

        return self.regroup(jnp.sum(self.array, axis=axis))

    def __next__(self):
        if self._current_index < self._length:
            # if self._is_numeric:
            #     new_grp = [self.grp[self._current_index]]  # [jnp.newaxis, ...]
            # else:
            #    new_grp = [self.grp[self._current_index]]

            item = self[self._current_index]
            # type(self)(
            #     gid=self.gid[self._current_index][jnp.newaxis, ...],
            #     grp=[self.grp[self._current_index]],
            # )

            self._current_index += 1

            return item
        else:
            self._current_index = 0

        raise StopIteration

    def __getitem__(self, index):
        cls = type(self)

        if isinstance(index, str):
            item = self.__getitem_str_(index)

        elif isinstance(index, slice):
            item = self.__getitem_slice_(index)

        elif isinstance(index, (list, Array)):
            item = self.__getitem_list_(index)

        elif isinstance(index, tuple):
            _next_index = index[1:]
            _current_item = self[index[0]]

            if _next_index:
                if isinstance(_current_item[0], SFXGroup):
                    _current_gid = _current_item.gid
                    item = type(_current_item)(
                        gid=_current_gid,
                        grp=[_ci.__getitem__(_next_index) for _ci in _current_item],
                    )
                elif hasattr(_current_item, "__getitem__"):
                    item = _current_item[_next_index]
                else:
                    item = _current_item
            else:
                item = _current_item

        elif isinstance(index, int) or any(
            map(lambda x: x == index.dtype, (jnp.int32, jnp.int64))
        ):
            item = self.__getitem_int_(index)

        else:
            raise TypeError(
                f"{cls.__name__} indices must be integers, slices or strings."
            )

        return item

    def __getitem_str_(self, string: str):
        # _get_gid = self._encode_gid(string)
        # _length = len(_get_gid)

        # if _get_gid.shape > self.gid.shape[1:]:
        #     condition = False
        # else:
        # We use this mapping as we compare arrays which truth can be ambiguous.
        is_gid = list(
            map(
                # lambda gid: all(_get_gid == gid[:_length])
                # & all(gid[_length:] == ord(" ")),
                lambda name: name.startswith(string),
                self.name,
            )
        )
        condition = any(is_gid)

        if condition:
            index = is_gid.index(True)
            return self.grp[index]
        else:
            raise KeyError(
                f"No such attribute: {string}. Possible attributes are: {', '.join(self.name)}"
            )

    def __getitem_int_(self, index: int):
        if index < len(self):
            return self.grp[index]

        else:
            raise IndexError(
                f"Index out of range; got {index} while length is {len(self)}"
            )

    def __getitem_slice_(self, slc: slice):
        if len(self) == 1:
            # When there is only one element, we check that the slice
            # contains that element and return it.
            # Otherwise we return an empty element
            if (
                slc.start is None
                or slc.start < len(self)
                and (slc.stop is None or slc.stop > len(self))
                and (slc.step is None or slc.step % 2 == 0)
            ):
                item = self.__getitem_int_(0)
            else:
                cls = type(self)
                item = cls(gid=[], grp=[])
        else:
            cls = type(self)
            item = cls(gid=self.gid[slc], grp=self.grp[slc])

        return item

    def __getitem_list_(self, index: list | Array):
        if max(index) < len(self):
            if isinstance(self.grp, jax.Array):
                if isinstance(index, Array):
                    items = self.grp[index]

                else:
                    items = self.grp[jnp.asarray(index, dtype=jnp.int32)]
            else:
                _tmp_gid = []
                _tmp_grp = []
                for i in index:
                    _tmp_gid.append(self.gid[i])
                    _tmp_grp.append(self.grp[i])
                items = type(self)(gid=_tmp_gid, grp=_tmp_grp)
            return items

        else:
            raise IndexError(
                f"Index out of range; got {index} while length is {len(self)}"
            )

    def __iadd__(self, other):
        cls = type(self)

        assert isinstance(
            other, type(self)
        ), f"Right-hand side should be a {cls.__name__}, not {type(other).__name__}"

        new_gid = self.name + other.name

        if isinstance(self.grp, jax.Array):
            new_grp = jnp.append(self.grp, jnp.asarray(other.grp), axis=0)
        else:
            new_grp = list(self.grp) + list(other.grp)

        return cls(**dict(gid=new_gid, grp=new_grp))

    def __add__(self, other):
        _cls = type(self)

        assert isinstance(
            other, type(self)
        ), f"Left- and right-side should be of the same type; Got {_cls.__name__} + {type(other).__name__}"
        # Temporary object of type cls that will contain the result of the
        # addition
        _temp = _cls(
            **{
                attr: self.__getattribute__(attr)
                for attr in self._getattrs(internal=False)
            }
        )
        _temp += other

        return _temp

    def __mul__(self, other):
        cls = type(self)

        assert isinstance(
            other, cls
        ), f"Left- and right-side for multiplication should be of the same type; Got {cls.__name__} * {type(other).__name__}"

        return cls(
            gid=self.gid,
            grp=[
                cls(
                    gid=other.gid,
                    grp=[
                        (
                            g1 * g2
                            # We check the type to make sure the __mul__ operator is supported
                            if isinstance(g1, (SFXGroup, jax.Array))
                            and type(g1) == type(g2)
                            else [g1, g2]
                        )
                        for g2 in other.grp
                    ],
                )
                for g1 in self.grp
            ],
        )

    # def __mul__(self, other):
    #     cls = type(self)
    #
    #     assert isinstance(
    #         other, cls
    #     ), f"Left- and right-side for multiplication should be of the same type; Got {cls.__name__} * {type(other).__name__}"
    #
    #     return cls(
    #         gid=self.gid,
    #         grp=[
    #             cls(
    #                 gid=other.gid,
    #                 grp=[
    #                     g1 * g2
    #                     # We check the type to make sure the __mul__ operator is supported
    #                     if isinstance(g1, (SFXGroup, jax.Array))
    #                     and type(g1) == type(g2)
    #                     else [g1, g2]
    #                     for g2 in other.grp
    #                 ],
    #             )
    #             for g1 in self.grp
    #         ],
    #     )

    def __repr__(self, _jax_compatible=False):
        clsname = self.__class__.__name__

        # if _jax_compatible:
        #     if self.gid.ndim > 1:
        #         clsparams = ", ".join(
        #             [f"{gid}={self.grp[i]}" for i, gid in enumerate(self.gid)]
        #         )
        #
        #     else:
        #         clsparams = f"{self.gid}={self.grp}"
        #
        # else:
        if isinstance(self.name, list):
            clsparams = ",".join(
                [f"{name}={self.grp[i]}" for i, name in enumerate(self.name)]
            )
        else:
            clsparams = f"{self.name}={self.grp}"

        return f"{clsname}({clsparams})"

    def map(
        self,
        func: Callable,
        condition: Callable = lambda _: False,
        *args,
        **kwargs,
    ):
        return self.regroup(self._map(self, func, condition, *args, **kwargs))

    def _map(
        self,
        node,
        func: Callable,
        condition: Callable,
        *args,
        _tree=None,
        **kwargs,
    ):
        if _tree is None:
            _tree = []

        if not hasattr(node, "grp") or condition(node):
            return func(node, *args, **kwargs)
        else:
            for n in node.grp:
                _tree.append(self._map(n, func, condition, *args, _tree=[], **kwargs))

        return _tree

    def vmap(
        self,
        func: Callable,
        depth,
        *args,
        **kwargs,
    ):
        if self.is_numeric:
            _func = self._vmap(
                func,
                depth,
                self.array,
                *args,
            )
            output = _func(self.array, *(arg.array for arg in args), kwargs)

        else:
            output = None
            raise RuntimeError("vmap can only be run on numeric groups.")

        return output

    def _vmap(
        self,
        _func,
        depth,
        *args,
        _depth=0,
    ):
        _length = len(args)

        if _depth == 0:

            def _new_func(*args):
                return _func(*args[:_length], **args[_length])

            if _depth == depth:
                func = jax.vmap(_new_func, in_axes=[0] * _length + [None])
            else:
                func = self._vmap(_new_func, depth, *args, _depth=_depth + 1)

        elif _depth < depth:
            _func = jax.vmap(_func, in_axes=[0] * _length + [None])
            func = self._vmap(_func, depth, *args, _depth=_depth + 1)
        else:
            func = jax.vmap(_func, in_axes=[0] * _length + [None])

        return func

    def tree_flatten_with_keys(self):
        _aux_data = tuple(self._getattrs(internal=False))
        children_with_keys = tuple(
            (attr, self.__getattribute__(attr)) if attr != "gid" else (attr, None)
            for attr in _aux_data
        )
        aux_data = (self.gid,)
        return (children_with_keys, aux_data)

    @classmethod
    def tree_unflatten(cls, aux_data, children):
        return cls(
            **{
                "gid": aux_data[-1],
                "grp": children[0],
            }
        )

    def tree_flatten(self):
        _aux_data = tuple(self._getattrs(internal=False))
        children = tuple(
            self.__getattribute__(attr)
            # else
            # (attr, None)
            for attr in _aux_data
            if attr != "gid"
        )
        aux_data = (self.gid,)
        return (children, aux_data)
