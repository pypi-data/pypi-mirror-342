# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import re
from collections.abc import Iterator
from typing import AnyStr

__all__: tuple[str, ...] = (
    "isplit",
    "must_split",
    "must_rsplit",
)


def isplit(source: AnyStr, sep=None, regex=False) -> Iterator[str]:
    """Generator of ``str.split()`` method.

    :param source: source string (unicode or bytes)
    :param sep: separator to split on.
    :param regex: if True, will treat sep as regular expression.

    :returns:
        generator yielding elements of string.

    Examples:
        >>> list(isplit("abcb", "b"))
        ['a', 'c', '']
        >>> s = isplit("foo bar")
        >>> next(s)
        'foo'
        >>> next(s)
        'bar'
    """
    if sep is None:
        # mimic default python behavior
        source = source.strip()
        sep = "\\s+"
        if isinstance(source, bytes):
            sep = sep.encode("ascii")
        regex = True
    start = 0
    if regex:
        # version using re.finditer()
        if not hasattr(sep, "finditer"):
            sep = re.compile(sep)
        for m in sep.finditer(source):
            idx = m.start()
            assert idx >= start
            yield source[start:idx]
            start = m.end()
        yield source[start:]
    else:
        # version using str.find(), less overhead than re.finditer()
        sep_size = len(sep)
        while True:
            idx = source.find(sep, start)
            if idx == -1:
                yield source[start:]
                return
            yield source[start:idx]
            start = idx + sep_size


def must_split(
    source: str,
    sep: str = None,
    *,
    maxsplit: int = -1,
    mustsplit: bool = True,
) -> list[str]:
    """
    Examples:
        >>> must_split('asd|fasd', '|', maxsplit=2)
        ['asd', 'fasd', None]
        >>> must_split('data', '.', maxsplit=1)
        ['data', None]
        >>> must_split('data')
        ['data']
    """
    if maxsplit == -1 or not mustsplit:
        return source.split(sep, maxsplit)
    _old: list = source.split(sep, maxsplit)
    _result: list = [None] * ((maxsplit + 1) - len(_old))
    _old.extend(_result)
    return _old


def must_rsplit(
    source: str,
    sep: str = None,
    *,
    maxsplit: int = -1,
    mustsplit: bool = True,
) -> list[str]:
    """
    Examples:
        >>> must_rsplit('asd|foo', '|', maxsplit=2)
        [None, 'asd', 'foo']
        >>> must_rsplit('foo bar', maxsplit=1)
        ['foo', 'bar']
        >>> must_rsplit('foo bar', maxsplit=2, mustsplit=False)
        ['foo', 'bar']
        >>> must_rsplit('foo')
        ['foo']
    """
    if maxsplit == -1 or not mustsplit:
        return source.rsplit(sep, maxsplit=maxsplit)
    _old: list = source.rsplit(sep, maxsplit)
    _result: list = [None] * ((maxsplit + 1) - len(_old))
    _result.extend(_old)
    return _result
