from __future__ import annotations

from typing import (
    Any,
    Callable,
    NoReturn,
    Optional,
    Union,
)
from unittest import mock

import pytest
from ddeutil.core import (
    filter_dict,
    first,
    isinstance_check,
    onlyone,
    random_str,
    remove_pad,
    round_up,
)


def test_instance_check():
    assert isinstance_check("s", str)
    assert isinstance_check(["s"], list[str])
    assert isinstance_check(("s", "t"), tuple[str, ...])
    assert not isinstance_check(("s", "t"), tuple[str])
    assert isinstance_check({"s": 1, "d": "r"}, dict[str, Union[int, str]])
    assert isinstance_check("s", Optional[str])
    assert isinstance_check(1, Optional[Union[str, int]])
    assert not isinstance_check("s", list[str])
    assert isinstance_check([1, "2"], list[Union[str, int]])
    assert not isinstance_check("s", NoReturn)
    assert isinstance_check(None, NoReturn)
    assert isinstance_check("A", Any)
    assert isinstance_check([1, [1, 2, 3]], list[Union[list[int], int]])
    assert not isinstance_check([1], Union[str, int])
    assert isinstance_check((1, "foo", True), tuple[int, str, bool])


def test_instance_generic():
    def caller() -> str:
        return "Success"

    assert isinstance_check(caller, Callable[[], str])
    assert isinstance_check(caller, Callable[[str], str])
    assert not isinstance_check(caller(), Callable[[], str])


def test_round_up():
    assert round_up(1.00406, 2) == 1.01
    assert round_up(1.00001, 1) == 1.1
    assert round_up(1.00001, 0) == 2


def test_remove_pad():
    assert remove_pad("000") == "0"
    assert remove_pad("12") == "12"


def test_only_one_with_default():
    fix_list: list = ["a", "b", "c"]
    output_lists: list = ["a", "a", "a"]
    for index, _list in enumerate(
        [
            [
                "a",
                "e",
                "f",
            ],
            ["e", "f"],
            ["a", "b", "e"],
        ],
        start=0,
    ):
        assert output_lists[index] == onlyone(_list, fix_list)


def test_only_one_dynamic_type():
    assert 1 == onlyone((1, 2, 3), [1, 4, 5])
    assert 1 == onlyone([1, 4, 5], (1, 2, 3))
    assert "1" == onlyone("145", ("1", "2", "3"))

    with pytest.raises(TypeError):
        onlyone({1, 4, 5}, (1, 2, 3))


def test_first():
    assert first((1, 2, 3), condition=lambda _: _ % 2 == 0) == 2
    assert first(range(3, 100)) == 3

    with pytest.raises(StopIteration):
        first(())

    with pytest.raises(StopIteration):
        first([1, 3, 5], default=1, condition=lambda _: _ % 2 == 0)

    assert first([1, 3, 5], default=2, condition=lambda _: _ % 2 == 0) == 2


def test_filter_dict():
    assert filter_dict({"foo": "bar"}, excluded={"foo"}) == {}


@mock.patch("random.choices", return_value="AA145WQ2")
def test_random_string(m):
    assert m.mocked
    assert random_str() == "AA145WQ2"
