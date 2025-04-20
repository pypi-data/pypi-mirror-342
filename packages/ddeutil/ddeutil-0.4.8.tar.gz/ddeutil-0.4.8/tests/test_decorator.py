import time
from functools import partial

import ddeutil.core.decorator as decorator
import pytest


def test_deepcopy():
    @decorator.deepcopy
    def foo(a, b, c=None):  # pragma: no cov
        c = c or {}
        a[1] = 3
        b[2] = 4
        c[3] = 5
        return a, b, c

    aa = {1: 2}
    bb = {2: 3}
    cc = {3: 4}

    assert foo(aa, bb, cc) == ({1: 3}, {2: 4}, {3: 5})
    assert (aa, bb, cc) == ({1: 2}, {2: 3}, {3: 4})


def test_deepcopy_method():
    class Foo:  # pragma: no cov
        @decorator.deepcopy
        def foo(self, a, b=None):
            b = b or {}

            a[1] = 4
            b[2] = 5
            return a, b

    aa = {1: 2}
    bb = {2: 3}
    assert ({1: 4}, {2: 5}) == Foo().foo(aa, bb)
    assert ({1: 2}, {2: 3}) == (aa, bb)


def test_profile():

    def log_override(msg: str, keeping: list):  # pragma: no cov
        keeping.append(msg)
        print(msg)

    keeps: list[str] = []

    @decorator.profile(log=partial(log_override, keeping=keeps), waiting=2)
    def waiting():  # pragma: no cov
        time.sleep(5)

    waiting()  # pragma: no cov


def test_profile_raise():

    def log_override(msg: str, keeping: list):
        keeping.append(msg)
        print(msg)

    keeps: list[str] = []

    @decorator.profile(log=partial(log_override, keeping=keeps), waiting=2)
    def waiting():
        time.sleep(5)
        raise ValueError

    with pytest.raises(ValueError):
        waiting()
