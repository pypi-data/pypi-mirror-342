from unittest import mock

import pytest
from ddeutil.core import (
    must_bool,
    must_list,
    str2any,
    str2args,
    str2bool,
    str2dict,
    str2int_float,
    str2list,
)
from ddeutil.core.base.convert import revert_args


def test_str2bool():
    assert not str2bool()

    for s in ("true", "True", "1", "Y", "y", "yes", "Yes", "o", "O"):
        assert str2bool(s)

    for s in ("false", "False", "0", "N", "n", "no", "No", "x", "X"):
        assert not str2bool(s)

    assert not str2bool("Nop", force_raise=False)


def test_str2bool_raise():
    with pytest.raises(ValueError):
        str2bool("Nop")


def test_str2list():
    assert str2list() == []
    assert str2list('["a", "b", "c"]') == ["a", "b", "c"]
    assert str2list('["d""]', force_raise=False) == ['["d""]']
    assert str2list('"d""]', force_raise=False) == ['"d""]']

    with pytest.raises(ValueError):
        str2list('["d""]')

    with pytest.raises(ValueError):
        str2list('"d""]')

    with mock.patch("ddeutil.core.convert.ujson", None):
        with pytest.raises(ImportError):
            str2list('["d", "a"]')


def test_str2dict():
    assert str2dict() == {}
    assert str2dict('{"a": 1, "b": 2, "c": 3}') == {"a": 1, "b": 2, "c": 3}
    assert str2dict('{"d""', force_raise=False) == {0: '{"d""'}
    assert str2dict('{"d"}', force_raise=False) == {0: '{"d"}'}

    with pytest.raises(ValueError):
        str2dict('{"d""')

    with pytest.raises(ValueError):
        str2dict('{"d"}')


def test_str2int_float():
    assert str2int_float() == 0
    assert str2int_float("+3") == 3
    assert str2int_float("-5.00") == -5.0
    assert str2int_float("-3.01") == -3.01
    assert str2int_float("[1]") == "[1]"
    assert str2int_float("x0", force_raise=False) == "x0"

    with pytest.raises(ValueError):
        str2int_float("x0", force_raise=True)


def test_must_list():
    assert must_list("[1, 2, 3]") == [1, 2, 3]
    assert must_list() == []
    assert must_list([1, "foo"]) == [1, "foo"]


def test_must_bool():
    assert must_bool("1")
    assert not must_bool(0)
    assert not must_bool("[1, 2, 'foo']")
    assert not must_bool(None)


def test_str2any():
    assert str2any(22) == 22
    assert str2any("1245") == 1245
    assert str2any('"string"') == "string"
    assert str2any("[1, 2, 3]") == [1, 2, 3]
    assert str2any('{"key": "value"}') == {"key": "value"}
    assert str2any("1245.123") == 1245.123
    assert str2any("True")
    assert str2any("[1, 2") == "[1, 2"
    assert str2any("1.232.1") == "1.232.1"


def test_revert_args():
    assert revert_args(
        "value", 1, name="demo", _dict={"k1": "v1", "k2": "v2"}
    ) == (("value", 1), {"name": "demo", "_dict": {"k1": "v1", "k2": "v2"}})
    assert revert_args(1, 2, 3) == ((1, 2, 3), {})
    assert revert_args(foo="bar") == ((), {"foo": "bar"})


def test_str2args():
    assert str2args("'value', 1, name='demo'") == (
        ("value", 1),
        {"name": "demo"},
    )
    assert str2args("'value', 1, '[1, 3, \"foo\"]'") == (
        ("value", 1, '[1, 3, "foo"]'),
        {},
    )
    assert str2args(None) == ((None,), {})
