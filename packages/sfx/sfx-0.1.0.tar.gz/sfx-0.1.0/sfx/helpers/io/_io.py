"""Helpers with Input/Output stuff."""

__all__ = ["load", "save"]

import hickle as hkl


def load(filename: str):
    """Loads the object saved under filename.

    :param filename: Name of the file contatining the object to load

    :return: The loaded object
    """
    return hkl.load(filename)


def save(object, filename: str):
    """Saves the object under filename.

    :param object: Object to save
    :param filename: Name of the file that will contain the object

    :return: The loaded object
    """
    hkl.dump(object, filename)
