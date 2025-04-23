# encoding: utf-8
"""
Utilities and dump / load handlers for handling jax types with hickle.
"""

__all__ = []

import types
from functools import partial
from typing import Any, Callable, Tuple, TypedDict

import dill
# %% IMPORTS
import jax
import jax.numpy as jnp
import numpy as np
from h5py import AttributeManager, Dataset, Group
from hickle.helpers import PyContainer, no_compression
from hickle.loaders.load_builtins import ListLikeContainer
from hickle.lookup import LoaderManager
from jax.tree_util import Partial
from jaxlib.xla_extension import ArrayImpl, PjitFunction

CreateDataSetOutput = Tuple[Dataset, Tuple[()]]
CreateGroupOutput = Tuple[Group, Tuple[str, Any, dict, dict]]

# %% FUNCTION DEFINITIONS

###############################################################################
#############################                    ##############################
#############################     JAX Arrays     ##############################
#############################                    ##############################
###############################################################################

### Create dataset functions ###


def create_jnp_scalar_dataset(
    py_obj: Any, h_group: Group, name: str, **kwargs: TypedDict
) -> CreateDataSetOutput:
    """Dumps a jax.numpy.scalar object to h5py file.

    :param py_obj: Python object to dump; should be a jax.numpy scalar, e.g.  jax.numpy.float16(1)
    :type  py_obj: jax.numpy.scalar

    :param h_group: Group to dump data into.
    :param name: The name of the resulting dataset.
    :param kwargs: Keyword arguments to be passed to create_dataset function.

    :return: tuple containing h5py.Dataset and empty list of subitems
    """

    d = h_group.create_dataset(name, data=np.asarray(py_obj), **no_compression(kwargs))

    d.attrs["jnp_dtype"] = py_obj.dtype.str.encode("ascii")
    return d, ()


def create_jnp_dtype(
    py_obj: Any, h_group: Group, name: str, **kwargs: TypedDict
) -> CreateDataSetOutput:
    """Dumps a jax.numpy.dtype object to h5py file.

    :param py_obj: Python object to dump; should be a jax.numpy dtype, e.g.  jax.numpy.float16
    :type  py_obj: jax.numpy.dtype

    :param h_group: Group to dump data into.
    :param name: The name of the resulting dataset.
    :param kwargs: Keyword arguments to be passed to create_dataset function.

    :return: tuple containing h5py.Dataset and empty list of subitems
    """
    d = h_group.create_dataset(name, data=bytearray(py_obj.str, "ascii"), **kwargs)
    return d, ()


def create_jnp_array_dataset(
    py_obj: Any, h_group: Group, name: str, **kwargs: TypedDict
) -> CreateDataSetOutput | CreateGroupOutput:
    """Dumps a jax.numpy.ndarray object to h5py file.

    :param py_obj: Python object to dump; should be a jax.numpy.ndarray

    :param h_group: Group to dump data into.

    :param name: The name of the resulting dataset.

    :param kwargs: Keyword arguments to be passed to create_dataset function.

    :return: Tuple containing ``h5py.Group`` and empty list of subitems.
    """

    # Obtain dtype of py_obj
    dtype = py_obj.dtype

    h_node = h_group.create_dataset(
        name,
        data=np.asarray(py_obj),
        **(no_compression(kwargs) if "bytes" in dtype.name else kwargs)
    )
    h_node.attrs["jnp_dtype"] = dtype.str.encode("ascii")
    return h_node, ()


def load_jnp_dtype_dataset(
    h_node: Dataset, base_type: bytes, py_obj_type: jnp.dtype
) -> jnp.dtype:
    """Restores dtype from dataset.

    :param h_node: The hdf5 node to load data from.
    :param base_type: Bytes string denoting base_type.
    :param py_obj_type: Final type of restored dtype.

    :return: Resulting jax.numpy.dtype.
    """
    return jnp.dtype(bytes(h_node[()]))


### Load dataset functions ###


def load_jnp_scalar_dataset(
    h_node: Dataset, base_type: bytes, py_obj_type: jnp.dtype
) -> jnp.dtype:
    """Restores scalar value dtype from dataset.

    :param h_node: The hdf5 node to load data from.
    :param base_type: Bytes string denoting base_type.
    :param py_obj_type: Final type of restored dtype.

    :return: Resulting jax.numpy.scalar.
    """

    dtype = jnp.dtype(h_node.attrs["jnp_dtype"])
    return dtype.type(h_node[()])


def load_ndarray_dataset(
    h_node: Dataset, base_type: bytes, py_obj_type: jnp.ndarray
) -> jax.Array:
    """Restores ndarray from dataset.

    :param h_node: The hdf5 node to load data from.
    :param base_type: Bytes string denoting base_type.
    :param py_obj_type: Final type of restored ndarray.

    :return: Resulting jax.numpy.ndarray.
    """
    dtype = jnp.dtype(h_node.attrs["jnp_dtype"])
    return jnp.asarray(h_node[()], dtype=dtype)


### Container ###


class NDArrayLikeContainer(ListLikeContainer):
    """
    PyContainer used to restore complex ndarray from h5py.Group node
    """

    __slots__ = ()

    def append(self, name: str, item: Any, h5_attrs: AttributeManager):
        # if group contains only one item which either has been
        # dumped using create_pickled_dataset or its name reads
        # data than assume single non list-type object otherwise
        # pass item on to append method of ListLikeContainer
        if h5_attrs.get("base_type", "") == b"pickle" or name == "data":
            self._content = item
        else:
            super(NDArrayLikeContainer, self).append(name, item, h5_attrs)

    def convert(self):
        data = jnp.asarray(self._content, dtype=self._h5_attrs["jnp_dtype"])
        return (
            data
            if data.__class__ is self.object_type
            or isinstance(self.object_type, types.LambdaType)
            else self.object_type(data)
        )


###############################################################################
#############################                    ##############################
#############################     JAX Arrays     ##############################
#############################                    ##############################
###############################################################################


def create_dilled_dataset(py_obj, h_group, name, reason=None, **kwargs):
    """
    Create pickle string as object can not be mapped to any other h5py
    structure.
    Parameters
    ----------
    py_obj:
        python object to dump; default if item is not matched.
    h_group (h5.File.group):
        group to dump data into.
    name (str):
        the name of the resulting dataset
    reason (str,None):
        reason why py_object has to be pickled eg. string
        provided by NotHicklable exception
    Warnings
    -------
    SerializedWarning:
        issued before pickle string is created
    """

    # store object as pickle string
    pickled_obj = dill.dumps(py_obj)
    d = h_group.create_dataset(name, data=memoryview(pickled_obj), **kwargs)
    return d, ()


def load_dilled_dataset(h_node, base_type, py_obj_type):
    """
    loade pickle string and return resulting py_obj
    """
    try:
        return dill.loads(h_node[()])
    except (ImportError, AttributeError):
        return None


#####################
# Lookup dictionary #
#####################

# %% REGISTERS
class_register = [
    [jnp.dtype, b"jnp_dtype", create_jnp_dtype, load_jnp_dtype_dataset],
    [
        jnp.number,
        b"jnp_scalar",
        create_jnp_scalar_dataset,
        load_jnp_scalar_dataset,
        None,
        False,
    ],
    # for all scalars which are not derived from jax.numpy.number which itself is jax.numpy.generic subclass
    # to properly catch and handle they will be caught by the following
    [
        jnp.generic,
        b"jnp_scalar",
        create_jnp_scalar_dataset,
        load_jnp_scalar_dataset,
        None,
        False,
    ],
    [
        jnp.ndarray,
        b"jnp_ndarray",
        create_jnp_array_dataset,
        load_ndarray_dataset,
        NDArrayLikeContainer,
    ],
    [
        ArrayImpl,
        b"ArrayImpl",
        create_jnp_array_dataset,
        load_ndarray_dataset,
        NDArrayLikeContainer,
    ],
    # [
    #    jnp.DeviceArray,
    #    b"DeviceArray",
    #    create_jnp_array_dataset,
    #    load_ndarray_dataset,
    #    NDArrayLikeContainer,
    # ],
    # [
    #     CompiledFunction,
    #     b"CompiledFunction",
    #     create_dilled_dataset,
    #     load_dilled_dataset,
    # ],
    [
        partial,
        b"partial",
        create_dilled_dataset,
        load_dilled_dataset,
    ],
    [
        PjitFunction,
        b"PjitFunction",
        create_dilled_dataset,
        load_dilled_dataset,
    ],
    [
        Partial,
        b"Partial",
        create_dilled_dataset,
        load_dilled_dataset,
    ],
]

for register in class_register:
    LoaderManager.register_class(*register)

exclude_register = []

# jax.config.update("jax_array", False)
