import pytest
from ddeutil.core import getdot, hasdot, setdot


def test_hasdot():
    assert hasdot("data.value", {"data": {"value": 2}})
    assert not hasdot("data.value.key", {"data": {"value": 2}})
    assert not hasdot("item.value.key", {"data": {"value": 2}})
    assert hasdot("1", {"1": True})


def test_getdot():
    assert getdot("data.value", {"data": {"value": 1}}) == 1
    assert getdot("data", {"data": "test"}) == "test"

    with pytest.raises(ValueError):
        getdot("data.value", {"data": "test"})

    with pytest.raises(ValueError):
        getdot("data.value", {"foo": "test"})

    with pytest.raises(ValueError):
        getdot("data.value.foo", {"data": {"value": [1, 2, 3]}})

    assert getdot("data.value", {"foo": "test"}, 1) == 1
    assert getdot("data.value", {"foo": "test"}, ignore=True) is None
    assert getdot("data.value", {"data": {"key": 1}}, None) is None
    assert (
        getdot("data.value.foo", {"data": {"value": [1, 2, 3]}}, ignore=True)
        is None
    )

    assert (
        getdot(
            "data.value.getter",
            {"data": {"value": {"getter": "success", "put": "fail"}}},
        )
        == "success"
    )

    assert getdot("foo.bar", {"foo": {"baz": 1}}, ignore=True) is None
    assert getdot("foo.bar", {"foo": {"bar": [1, 2, 3]}}) == [1, 2, 3]

    assert getdot("foo.bar", {"foo": {"baz": 1}}, 2, 3) == 2
    assert getdot("foo.bar", {"foo": {"baz": 1}}, 2, 3, ignore=True) == 2

    assert getdot("test?.error", {"foo": "bar"}) is None
    assert getdot("test.error?.message", {"test": {"bar": {}}}) is None

    assert getdot("value", [1, 2, 3], ignore=True) is None
    assert getdot("value", [1, 2, 3], 2) == 2

    with pytest.raises(ValueError):
        assert getdot("value", [1, 2, 3])

    assert getdot("value.1.foo", {"value": {1: {"foo": "bar"}}}) == "bar"
    assert getdot("value.0", {"value": {0: {"foo": "bar"}}}) == {"foo": "bar"}
    assert getdot("1", {"1": 100}) == 100
    assert getdot("1", {1: 100}) == 100
    assert getdot("1", {1.0: 100}, ignore=True) == 100
    assert getdot("1", {1.1: 100}, ignore=True) is None
    assert getdot("1.1", {1.1: 100}, ignore=True) is None


def test_setdot():
    assert setdot("data.value", {"data": {"value": 1}}, 2) == {
        "data": {"value": 2}
    }
    assert setdot("data.value.key", {"data": {"value": 1}}, 2, ignore=True) == {
        "data": {"value": 1}
    }

    with pytest.raises(ValueError):
        setdot("data.foo", {"data": {"value": 1}}, 10)

    with pytest.raises(ValueError):
        setdot("data.value.foo", {"data": {"value": [1, 2, 3]}}, 1)

    assert setdot("foo", {"data": {"value": 1}}, 10, ignore=True) == {
        "data": {"value": 1}
    }
