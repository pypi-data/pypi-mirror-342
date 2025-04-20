# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import copy
import logging
import time
from functools import wraps
from inspect import ismethod
from typing import TYPE_CHECKING, Callable, TypeVar

if TYPE_CHECKING:  # pragma: no cove
    import sys

    if sys.version_info >= (3, 10):
        from typing import ParamSpec
    else:
        from typing_extensions import ParamSpec

    P = ParamSpec("P")
    T = TypeVar("T")


STR_TYPES = (bytes, str)


def deepcopy(func: Callable[P, T]) -> Callable[P, T]:  # pragma: no cov
    """Deep-copy decorator for deep copy on the args and kwargs.

    Examples:
        >>> @deepcopy
        ... def foo(a, b, c=None):
        ...     c = c or {}
        ...     a[1] = 3
        ...     b[2] = 4
        ...     c[3] = 5
        ...     return a, b, c
        >>> aa = {1: 2}
        >>> bb = {2: 3}
        >>> cc = {3: 4}
        >>> foo(aa, bb, cc)
        ({1: 3}, {2: 4}, {3: 5})

        >>> (aa, bb, cc)
        ({1: 2}, {2: 3}, {3: 4})

        >>> class Foo:
        ...
        ...     @deepcopy
        ...     def foo(self, a, b=None):
        ...         b = b or {}
        ...         a[1] = 4
        ...         b[2] = 5
        ...         return a, b
        >>>
        >>> aa = {1: 2}
        >>> bb = {2: 3}
        >>> Foo().foo(aa, bb)
        ({1: 4}, {2: 5})

        >>> (aa, bb)
        ({1: 2}, {2: 3})
    """

    # NOTE: This condition use for a func that be method type.
    def method_get(self: object, *args: P.args, **kwargs: P.kwargs) -> T:
        return func(
            self,
            *(copy.deepcopy(x) for x in args),
            **{k: copy.deepcopy(v) for k, v in kwargs.items()},
        )

    def func_get(*args: P.args, **kwargs: P.kwargs) -> T:
        return func(
            *(copy.deepcopy(x) for x in args),
            **{k: copy.deepcopy(v) for k, v in kwargs.items()},
        )

    return method_get if ismethod(func) else func_get


def retry(
    max_attempts: int,
    delay: int = 1,
) -> Callable[[Callable[P, T]], Callable[P, T]]:  # pragma: no cove
    """Retry decorator with sequential.

    Examples:
        >>> @retry(max_attempts=3, delay=2)
        ... def fetch_data(url):
        ...     print("Fetching the data ...")
        ...     raise TimeoutError("Server is not responding.")
        >>> fetch_data("https://example.com/data")
        Fetching the data ...
        Attempt 1 failed: Server is not responding.
        Fetching the data ...
        Attempt 2 failed: Server is not responding.
        Fetching the data ...
        Attempt 3 failed: Server is not responding.
        Function `fetch_data` failed after 3 attempts
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            _attempts: int = 0
            while _attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    _attempts += 1
                    logging.info(f"Attempt {_attempts} failed: {e}")
                    if _attempts > 3:
                        time.sleep(delay + 2 ** (_attempts - 2))
                    else:
                        time.sleep(delay)
            logging.debug(
                f"Function `{func.__name__}` failed after "
                f"{max_attempts} attempts"
            )

        return wrapper

    return decorator


def profile(
    prefix: str = None, waiting: int = 10, log=None
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Profile memory and cpu that use on the current state."""
    from .threader import MonitorThread

    ts = time.monotonic()
    thread = MonitorThread(prefix=prefix, waiting=waiting, log=log)
    thread.start()

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return func(*args, **kwargs)
            finally:
                padded_name: str = "Time execute ".ljust(60, ".")
                padded_time: str = f" {(time.monotonic() - ts):0.2f}".rjust(
                    6, "."
                )
                print(f"{padded_name}{padded_time}s", flush=True)

                thread.stop()
                cpu, mem = thread.summarize
                print(f"Summary CPU%: {cpu}, Mem%: {mem}")

        return wrapper

    return decorator
