# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import ast
from typing import (
    Any,
    Optional,
    Union,
)

try:
    import ujson
except ImportError:  # pragma: no cove
    ujson = None

try:
    from .checker import FalseStr, TrueStr
except ImportError:  # pragma: no cove
    raise ImportError("This module need checker module.") from None

__all__: tuple[str, ...] = (
    "must_list",
    "must_bool",
    "str2bool",
    "str2list",
    "str2dict",
    "str2any",
    "str2args",
    "str2int_float",
    "revert_args",
)


def str2bool(
    value: Optional[str] = None,
    force_raise: bool = True,
) -> bool:
    """Convert an input string value to boolean (True or False).

    Examples:
        >>> str2bool('yes')
        True
        >>> str2bool('false')
        False
        >>> str2bool('0')
        False
    """
    value = value or ""
    if not value:
        return False
    elif value.lower() in TrueStr:
        return True
    elif value.lower() in FalseStr:
        return False
    if force_raise:
        raise ValueError(f"value {value!r} does not convert to boolean type")
    return False


def str2list(
    value: Optional[str] = None,
    force_raise: bool = True,
) -> list[Any]:
    """Convert an input string value to list.

    Examples:
        >>> str2list('["a", "b", "c"]')
        ['a', 'b', 'c']
        >>> str2list('["d""]', force_raise=False)
        ['["d""]']
        >>> str2list('["d""]')
        Traceback (most recent call last):
        ...
        ValueError: can not convert string value '["d""]' to list object
    """
    if value is None or value == "":
        return []

    if not value.startswith("[") or not value.endswith("]"):
        if force_raise:
            raise ValueError(
                f"can not convert string value {value!r} to list object"
            )
        return [value]

    if ujson is None:
        raise ImportError(
            "This function want to use ujson package for dumps values, "
            "`pip install ddeutil[all]`."
        )
    try:
        # ISSUE: When we talk about performance;
        # - ast.literal_eval(value) handler error SyntaxError (slower)
        return ujson.loads(value)
    except ujson.JSONDecodeError as err:
        if force_raise:
            raise ValueError(
                f"can not convert string value {value!r} to list object"
            ) from err
        return [value]


def str2dict(
    value: Optional[str] = None,
    force_raise: bool = True,
) -> dict[Any, Any]:
    """Convert an input string value to dict.

    Examples:
        >>> str2dict('{"a": 1, "b": 2, "c": 3}')
        {'a': 1, 'b': 2, 'c': 3}
        >>> str2dict('{"d""}', force_raise=False)
        {0: '{"d""}'}
        >>> str2dict('{"d""}')
        Traceback (most recent call last):
        ...
        ValueError: can not convert string value '{"d""}' to dict object
    """
    if value is None or value == "":
        return {}

    if not value.startswith("{") or not value.endswith("}"):
        if force_raise:
            raise ValueError(
                f"can not convert string value {value!r} to dict object"
            )
        return {0: value}

    try:
        rs = ast.literal_eval(value)
        if isinstance(rs, set):
            raise ValueError("Expect string of dict type result not set")
        return rs
    except (SyntaxError, ValueError) as err:
        if force_raise:
            raise ValueError(
                f"can not convert string value {value!r} to dict object"
            ) from err
        return {0: value}


def str2int_float(
    value: Optional[str] = None,
    force_raise: bool = False,
) -> Union[int, float, str]:
    """Convert an input string value to int or float.

    Examples:
        >>> str2int_float('12')
        12
        >>> str2int_float('+3')
        3
        >>> str2int_float('-5.00')
        -5.0
        >>> str2int_float('-3.01')
        -3.01
        >>> str2int_float('[1]')
        0
        >>> str2int_float('x0', force_raise=True)
        Traceback (most recent call last):
        ...
        ValueError: can not convert string value 'x0' to int or float
    """
    if value is None or value == "":
        return 0
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError as err:
            if not force_raise:
                return value
            raise ValueError(
                f"can not convert string value {value!r} to int or float"
            ) from err


def must_list(value: Optional[Union[str, list[Any]]] = None) -> list[Any]:
    """Return the list value that was converted from string or list value.

    :param value: A value that will validate and force to list value.
    :type value: str | list[Any] | None

    :rtype: list[Any]

    Examples:
        >>> must_list('[1, 2, 3]')
        [1, 2, 3]
        >>> must_list(None)
        []
    """
    if value:
        return str2list(value) if isinstance(value, str) else value
    return []


def must_bool(
    value: Optional[Union[str, int, bool]] = None,
    force_raise: bool = False,
) -> bool:
    """Return the boolean value that was converted from string, integer,
    or boolean value.

    Examples:
        >>> must_bool('1')
        True
        >>> must_bool(0)
        False
        >>> must_bool("[1, 2, 'foo']")
        False
        >>> must_bool(None)
        False
    """
    if value:
        return (
            value
            if isinstance(value, bool)
            else str2bool(str(value), force_raise=force_raise)
        )
    return False


def str2any(value: str) -> Any:
    """Convert an input string value to the real type of that object. Note that
    this convert function do not force or try-hard to convert type such as a
    boolean value should be 'True' or 'False' only.

    :param value: An any string value that want to convert.
    :rtype: Any

    Examples:
        >>> str2any('1245')
        1245
        >>> str2any('"string"')
        'string'
        >>> str2any('[1, 2, 3]')
        [1, 2, 3]
        >>> str2any('{"key": "value"}')
        {'key': 'value'}
        >>> str2any('1245.123')
        1245.123
        >>> str2any('True')
        True
    """
    if not isinstance(value, str):
        return value
    elif value.startswith(('"', "'")) and value.endswith(('"', "'")):
        return value.strip("\"'")
    elif value.startswith("[") and value.endswith("]"):
        return str2list(value)
    elif value.startswith("{") and value.endswith("}"):
        return str2dict(value)
    elif value in ("True", "False"):
        return str2bool(value)
    else:
        try:
            return str2int_float(value, force_raise=True)
        except ValueError:
            return value


def revert_args(*args, **kwargs) -> tuple[tuple[Any], dict[Any, Any]]:
    """Return arguments and key-word arguments.

    Examples:
        >>> revert_args('value', 1, name='demo', _dict={'k1': 'v1', 'k2': 'v2'})
        (('value', 1), {'name': 'demo', '_dict': {'k1': 'v1', 'k2': 'v2'}})
        >>> revert_args(1, 2, 3)
        ((1, 2, 3), {})
        >>> revert_args(foo='bar')
        ((), {'foo': 'bar'})
    """
    return args, kwargs


def str2args(value: Optional[str]) -> tuple[tuple[Any], dict[Any, Any]]:
    """Convert an input string to args and kwargs values.

    Examples:
        >>> str2args("'value', 1, name='demo'")
        (('value', 1), {'name': 'demo'})
        >>> str2args("'value', 1, '[1, 3, \\"foo\\"]'")
        (('value', 1, '[1, 3, "foo"]'), {})
        >>> str2args()
        ((None,), {})
    """
    return eval(f"revert_args({value})")
