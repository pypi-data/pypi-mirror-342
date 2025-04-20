from functools import lru_cache
from unittest import mock

import pytest
from ddeutil.core.base.hash import (
    checksum,
    freeze_args,
    hash_str,
    hash_value,
)


def test_hash_str():
    assert "05751529" == hash_str("hello world")
    assert "105751529" == hash_str("hello world", n=9)
    assert (
        "838141983831025582197310782608927299322466180042657006854679"
        "28187377105751529"
    ) == hash_str("hello world", n=-1)

    with pytest.raises(ValueError):
        hash_str("hello world", n=-2)


def test_hash_all():
    assert {
        "dict": {
            "list": [
                "acbd18db4cc2f85cedef654fccc4a4d8",
                "37b51d194a7513e45b56f6524f2d51f2",
            ]
        },
        "bool": True,
        "none": None,
        "str": "acbd18db4cc2f85cedef654fccc4a4d8",
        "tuple": (
            "c4ca4238a0b923820dcc509a6f75849b",
            "c81e728d9d4c2f636f067f89cc14862c",
            "eccbc87e4b5ce2fe28308fd9f2a7baf3",
        ),
    } == hash_value(
        {
            "str": "foo",
            "bool": True,
            "none": None,
            "tuple": (
                1,
                2,
                3,
            ),
            "dict": {
                "list": ["foo", "bar"],
            },
        }
    )


def test_checksum():
    assert "83788ce748a5899920673e5a4384979b" == checksum(
        {"foo": "bar", "baz": 1}
    )

    with mock.patch("ddeutil.core.hash.ujson", None):
        with pytest.raises(ImportError):
            checksum({"foo": "bar", "baz": 1})


def test_freeze_args():

    @freeze_args
    @lru_cache
    def cache_func(x, y):
        return x, y

    cache_func({"data": [1, 2, 3, 4]}, ["a", "b", "c"])
