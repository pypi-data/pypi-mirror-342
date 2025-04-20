# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import hashlib
from collections.abc import Collection
from functools import wraps
from typing import (
    Any,
    Optional,
)

try:
    import ujson
except ImportError:  # pragma: no cove
    ujson = None

__all__: tuple[str, ...] = (
    "checksum",
    "hash_value",
    "hash_str",
    "freeze",
    "freeze_args",
)


def checksum(value: dict[str, Any]) -> str:
    """Return a string of the hashing value by MD5 algorithm.

    :param value: A value that want to generate hash with md5.

    Examples:
        >>> checksum({"foo": "bar", "baz": 1})
        '83788ce748a5899920673e5a4384979b'
    """
    if ujson is None:
        raise ImportError(
            "This function want to use ujson package for dumps values, "
            "`pip install ddeutil[checksum]`."
        )
    return hashlib.md5(
        ujson.dumps(value, sort_keys=True).encode("utf-8")
    ).hexdigest()


def hash_value(
    value: Any,
    exclude: Optional[Collection] = None,
) -> Any:
    """Hash all values in dictionary and all elements in collection.

    Examples:
        >>> hash_value({'foo': 'bar'})
        {'foo': '37b51d194a7513e45b56f6524f2d51f2'}
    """
    _exclude_keys: Collection = exclude or set()
    if isinstance(value, dict):
        return {
            k: hash_value(v) if k not in _exclude_keys else v
            for k, v in value.items()
        }
    elif isinstance(value, (list, tuple)):
        return type(value)([hash_value(i) for i in value])
    elif isinstance(value, bool):
        return value
    elif isinstance(value, (int, float)):
        value = str(value)
    elif value is None:
        return value
    return hashlib.md5(value.encode("utf-8")).hexdigest()


def hash_str(value: str, n: int = 8) -> str:
    """Hash str input to number with SHA256 algorithm
    more algoritm be md5, sha1, sha224, sha256, sha384, sha512

    Examples:
        >>> hash_str('Hello World')
        '40300654'
        >>> hash_str('hello world')
        '05751529'
    """
    if n < -1 or n >= 16:
        raise ValueError(
            "Number of hashing string function does not support less than -1, "
            "or rather than 16 digit."
        )
    hasted: str = str(
        int(hashlib.sha256(value.encode("utf-8")).hexdigest(), 16)
    )
    if n == -1:
        return hasted
    return hasted[-n:]


def freeze(value: Any) -> Any:  # pragma: no cove
    """Freeze a value to immutable object.
    Examples:
        >>> freeze({'foo': 'bar'})
        frozenset({('foo', 'bar')})
        >>> freeze('foo')
        'foo'
        >>> freeze(('foo', 'bar'))
        ('foo', 'bar')
    """
    if isinstance(value, dict):
        return frozenset((key, freeze(value)) for key, value in value.items())
    elif isinstance(value, list):
        return tuple(freeze(value) for value in value)
    elif isinstance(value, set):
        return frozenset(freeze(value) for value in value)
    return value


def freeze_args(func):  # pragma: no cove
    """Transform mutable dictionary into immutable useful to be compatible with
    cache.

    Examples:
        >>> from functools import lru_cache
        ... @lru_cache(maxsize=None)
        ... def call_name(value: dict):
        ...     return value['foo'] + " " + value['bar']
        ... call_name({'foo': 'Hello', 'bar': 'World'})
        Traceback (most recent call last):
        ...
        TypeError: unhashable type: 'dict'

        >>> @freeze_args
        ... @lru_cache(maxsize=None)
        ... def call_name(value: dict):
        ...     return value['foo'] + " " + value['bar']
        ... call_name({'foo': 'Hello', 'bar': 'World'})
        'Hello World'
    """

    class HashMixin:
        def __hash__(self):
            return hash(freeze(self))

    class HashDict(HashMixin, dict): ...

    class HashList(HashMixin, list): ...

    class HashSet(HashMixin, set): ...

    def map_hash(value: Any):
        if isinstance(value, dict):
            return HashDict(value)
        elif isinstance(value, list):
            return HashList(value)
        elif isinstance(value, set):
            return HashSet(value)
        return value

    @wraps(func)
    def wrapped(*args, **kwargs):
        args: tuple = tuple(map_hash(arg) for arg in args)
        kwargs: dict = {k: map_hash(v) for k, v in kwargs.items()}
        return func(*args, **kwargs)

    return wrapped
