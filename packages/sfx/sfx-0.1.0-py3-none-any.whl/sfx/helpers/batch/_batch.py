"""Helpers to batch process an operation."""

import multiprocessing as mp

__all__ = [
    "recursive_call",
    "recursive_call_multiprocess",
    "create_recursive_list",
    "get_number_batches",
]


def _is_leaf(node):
    return not isinstance(node, (list, tuple))


def recursive_call(
    func,
    obj,
    *args,
    **kwargs,
):
    if not isinstance(obj, (list, tuple)):
        yield func(obj, *args, **kwargs)
    else:
        for ob in obj:
            yield from recursive_call(func, ob, *args, **kwargs)


# def recursive_call(
#    func,  # =lambda x, *args, **kwargs: x,
#    obj,
#    *args,
#    _tree=None,
#    **kwargs,
# ):
#    if _tree is None:
#        _tree = []
#
#    if _is_leaf(obj):
#        return func(obj, *args, **kwargs)
#    else:
#        for ob in obj:
#            _tree.append(recursive_call(func, ob, _tree=[], *args, **kwargs))
#
#    return _tree


def _recursive_call_multiprocess(
    pool,
    func,  # =lambda x, *args, **kwargs: x,
    obj,
    *args,
    callback=None,
    error_callback=None,
    _tree=None,
    **kwargs,
):
    if _tree is None:
        _tree = []

    if _is_leaf(obj):
        _tree.append(
            pool.apply_async(
                func,
                (obj, *args),
                kwargs,
                callback,
                error_callback,
            )
        )
    else:
        for ob in obj:
            _recursive_call_multiprocess(
                pool,
                func,
                ob,
                *args,
                callback=callback,
                error_callback=error_callback,
                _tree=_tree,
                **kwargs,
            )

    return _tree


def recursive_call_multiprocess(
    func,
    obj,
    *args,
    callback=None,
    error_callback=None,
    _nbprocesses=None,
    _maxtaskperchild=2,
    **kwargs,
):
    with mp.Pool(processes=_nbprocesses, maxtasksperchild=_maxtaskperchild) as pool:
        _tree = _recursive_call_multiprocess(
            pool,
            func,
            obj,
            *args,
            callback=callback,
            error_callback=error_callback,
            **kwargs,
        )
        result = [t.get() for t in _tree]
    return result


def create_recursive_list(_dict=None, _tree=None, _depth=0, **kwargs):
    if _tree is None:
        _tree = []

    if _dict is None:
        _dict = dict()

    if _depth == len(kwargs):
        return _dict.copy()
    else:
        key = list(kwargs.keys())[_depth]
        for p in kwargs[key]:
            _dict[key] = p
            _tree.append(
                create_recursive_list(
                    _dict=_dict, _tree=[], _depth=_depth + 1, **kwargs
                )
            )

    return _tree


def get_number_batches(parameters):
    return sum(recursive_call(lambda _: 1, parameters))
