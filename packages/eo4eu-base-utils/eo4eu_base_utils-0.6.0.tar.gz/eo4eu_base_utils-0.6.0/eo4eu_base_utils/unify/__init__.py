import re
import functools
from types import UnionType
from ..typing import Any, Union, List, Dict, Iterable, get_origin, get_args
from ..result import Result


def overlay_pair(lhs: Any, rhs: Any) -> Any:
    """Recursively combines dictionaries and lists, favoring the second argument when necessary.
    The types of `lhs` and `rhs` MUST be the same.
    Lists are concatenated, while dictionaries are made into a union of both.

    :param lhs: First object
    :type lhs: Any
    :param rhs: Second object
    :type rhs: Any
    :returns: A dictionary/list with contents from both inputs
    :rtype: Any
    """
    if isinstance(lhs, list) and isinstance(rhs, list):
        return lhs + rhs

    if not (isinstance(lhs, dict) and isinstance(rhs, dict)):
        return rhs

    result = {key: val for key, val in lhs.items()}
    for key, val in rhs.items():
        if key not in result:
            result[key] = val
        else:
            result[key] = overlay(result[key], val)

    return result


def overlay(*args: Any) -> Any:
    """Applies `overlay_pair` to many inputs, one after another.
    This simply calls functools.reduce on `overlay_pair`

    :param args: The objects to be overlaid
    :type args: tuple[Any]
    :rtype: Any
    """
    return functools.reduce(overlay_pair, args)


def get_recursively(d: Dict, path: List[Any]) -> Any:
    """Gets items found in `path` from dict `d`

    :param d: An object implementing `__getitem__`
    :type d: Dict
    :param path: A list of nested dictionary keys
    :type path: List[Any]
    :raises: KeyError
    :return: The nested value
    :rtype: Any
    """
    result = d
    for key in path:
        result = result[key]
    return result


def set_recursively(d: Dict, path: List[Any], val: Any):
    """Sets values found in `path` into dict `d`

    :param d: An object implementing `__getitem__` and `__setitem__`
    :type d: Dict
    :param path: A list of nested dictionary keys
    :type path: List[Any]
    :raises: KeyError
    :return: Nothing
    :rtype: None
    """
    if len(path) == 0:
        return

    result = d
    head, tail = path[:-1], path[-1]
    for key in head:
        result = result[key]
    result[tail] = val


class UnifyError(Exception):
    """Generic exception thrown by :func:`eo4eu_base_utils.unify.unify`"""
    pass


def _unify_error(path: list[str], blurb: str):
    full_key = ".".join(path)
    if len(path) == 0:
        full_key = "."
    return Result.err(f"Key \"{full_key}\": {blurb}")


def _unify_types(lhs: Iterable[type], rhs: Any, path: list[str], name: str) -> Result:
    if isinstance(rhs, type) and (rhs not in lhs):
        return _unify_error(path, f"Type \"{rhs}\" incompatible with value \"{name}\"")
    elif not isinstance(rhs, lhs):
        return _unify_error(path, f"Value \"{rhs}\" incompatible with type \"{name}\"")
    return Result.ok(rhs)


def _unify_simple(lhs: Any, rhs: Any, path: list[str]) -> Result:
    if lhs != rhs:
        return _unify_error(path, f"Value \"{rhs}\" incompatible with \"{lhs}\"")
    return Result.ok(rhs)


def _unify_regex(lhs: re.Pattern, rhs: Any, path: list[str]) -> Result:
    if isinstance(rhs, re.Pattern):
        return _unify_scalar(lhs.pattern, rhs.patterns, path)
    if isinstance(rhs, str):
        if re.fullmatch(rhs) is None:
            return _unify_error(path, f"Value \"{rhs}\" incompatible with pattern \"{lhs.pattern}\"")
        return Result.ok(rhs)

    return _unify_error(path, f"Value \"{rhs}\" of type \"{rhs.__class__.__name__}\" cannot "
                              f"be matched to \"{lhs.pattern}\"")


def _unify_scalar_one_side(lhs: Any, rhs: Any, path: list[str]) -> tuple[Result,bool]:
    if isinstance(lhs, type):
        return (_unify_types((lhs,), rhs, path, str(lhs.__name__)), True)
    if get_origin(lhs) in (Union, UnionType):
        return (_unify_types(get_args(lhs), rhs, path, str(lhs)), True)
    if isinstance(lhs, re.Pattern):
        return (_unify_regex(lhs, rhs, path), True)
    return (None, False)


def _unify_scalar(lhs: Any, rhs: Any, path: list[str]) -> Result:
    result, ok = _unify_scalar_one_side(lhs, rhs, path)
    if not ok:
        result, ok = _unify_scalar_one_side(rhs, lhs, path)
    if not ok:
        return _unify_simple(lhs, rhs, path)
    return result


def _unify_dict(lhs: dict, rhs: Any, path: List[str], exit_on_err: bool = False) -> Result:
    if not isinstance(rhs, Dict):
        return _unify_error(path, f"Value \"{rhs}\" incompatible with type \"Dict\"")

    result_dict = {key: val for key, val in lhs.items()}
    error_stack = []
    for key, val in rhs.items():
        if key not in result_dict:
            result_dict[key] = val
        elif isinstance(val, Dict):
            unify_res = _unify_dict(result_dict[key], val, path + [key])
            if unify_res.is_ok():
                result_dict[key] = unify_res.get()
            else:
                error_stack.extend(unify_res.stack())
                if exit_on_err:
                    break
        else:
            unify_res = _unify_scalar(result_dict[key], val, path + [key])
            if unify_res.is_ok():
                result_dict[key] = unify_res.get()
            else:
                error_stack.extend(unify_res.stack())
                if exit_on_err:
                    break

    return Result(
        is_ok = len(error_stack) == 0,
        value = result_dict,
        stack = error_stack
    )


def _unify_pair(lhs: Any, rhs: Any, path: list[str], **kwargs) -> Result:
    if isinstance(lhs, Dict):
        return _unify_dict(lhs, rhs, path, **kwargs)
    if isinstance(rhs, Dict):
        return _unify_dict(rhs, lhs, path, **kwargs)
    return _unify_scalar(lhs, rhs, path)


def unify_pair(lhs: Any, rhs: Any, unwrap = True, **kwargs) -> Any:
    """Combines two values, checking whether they are "compatible".
    The values may be types, type unions, strings, regular expressions, or
    any generic value. Baiscally, unifying two objects means checking
    compatibility and choosing the most specific option. The rules are 
    more-or-less as follows:

    unify(type A, type B)  -> A if A == B, otherwise error

    unify(type union A, type B)  -> B if B in A, otherwise error

    unify(type A, value a) -> a if isinstance(a, A), otherwise error

    unify(type union A, value a) -> a if type(a) in A, otherwise error

    unify(regex A, string a) -> a if regex matches a, otherwise error

    unify(dict, A, dict B) -> A union of the two dicts, where all values
    which exist on both (including nested dicts) are unified

    This function is meant to be commutative, meaning

    unify(a, b) == unify(b, a)

    :param lhs: The left value
    :type lhs: Any
    :param rhs: The right value
    :type rhs: Any
    :param unwrap: Whether to unwrap the result. If True, a :class:`eo4eu_base_utils.unify.UnifyError` is raised if there is an error. Otherwise, a :class:`eo4eu_base_utils.result.Result` with the value is returned.
    :type unwrap: bool
    :param kwargs: Other arguments passed to the underlying functions. Only important one currently is `exit_on_err`, which will make the function exit whenever an error is encountered. Otherwise, it keeps going and records all errors it found. Default is True
    :type kwargs: Dict
    :raises: :class:`UnifyError` if `unwrap` is True
    :returns: The union of `lhs` and `rhs`
    :rtype: Any
    """
    result = _unify_pair(lhs, rhs, [], **kwargs)
    if unwrap:
        return result.unwrap(exc_class = UnifyError)
    return result


def unify(*args: Any, **kwargs) -> Any:
    """Applies :func:`unify_pair` to many inputs, one after another.
    This simply calls functools.reduce on :func:`unify_pair`

    :param args: The objects to be unified
    :type args: tuple[Any]
    :param kwargs: Optional keyword arguments passed to :func:`unify_pair`
    :type args: Dict
    :raises: :class:`UnifyError` if `unwrap` is True
    :rtype: Any
    """
    return functools.reduce(
        functools.partial(unify_pair, **kwargs),
        args
    )
