import pytest
from ddeutil.core import merge


def test_zip_equal():
    assert list(merge.zip_equal((1, 2, 3, 4), ("a", "b", "c", "d"))) == [
        (1, "a"),
        (2, "b"),
        (3, "c"),
        (4, "d"),
    ]
    assert next(merge.zip_equal((1, 2, 3, 4), ("a", "b", "c"))) == (1, "a")

    with pytest.raises(ValueError):
        list(
            merge.zip_equal(
                (1, 2, 3, 4),
                ("a", "b", "c"),
            )
        )


def test_merge_dict():
    dicts = [{"A": 1, "B": 2}, {"A": 10, "C": 30}, {"C": 300, "D": 400}]

    assert merge.merge_dict(*dicts, mode="chain") == {
        "A": 10,
        "B": 2,
        "C": 300,
        "D": 400,
    }
    assert merge.merge_dict(*dicts, mode="update") == {
        "A": 10,
        "B": 2,
        "C": 300,
        "D": 400,
    }
    assert merge.merge_dict(*dicts, mode="reduce") == {
        "A": 10,
        "B": 2,
        "C": 300,
        "D": 400,
    }
    assert merge.merge_dict(*dicts, mode="foo") == dicts


def test_merge_list():
    lists: list[list[str]] = [
        ["A", "B", "C"],
        ["C", "D", "E"],
    ]
    assert merge.merge_list(*lists, mode="extend") == [
        "A",
        "B",
        "C",
        "C",
        "D",
        "E",
    ]
    assert merge.merge_list(*lists, mode="reduce") == [
        "A",
        "B",
        "C",
        "C",
        "D",
        "E",
    ]

    assert merge.merge_list(*lists, mode="foo") == lists


def test_merge_dict_value():
    assert merge.merge_dict_value({"a": 1, "b": 5}, {"a": 3, "b": 6}) == {
        "a": [1, 3],
        "b": [5, 6],
    }
    assert merge.merge_dict_value({"a": 1}, {"a": 3, "b": 6}) == {
        "a": [1, 3],
        "b": [6],
    }
    assert merge.merge_dict_value(
        {"a": 1}, {"a": 1, "b": 6}, duplicate=False
    ) == {
        "a": {1},
        "b": {6},
    }
    assert merge.merge_dict_value(
        {"a": 1, "b": 5}, {"a": 3, "b": 6}, mode="foo"
    ) == [{"a": 1, "b": 5}, {"a": 3, "b": 6}]


def test_merge_dict_value_list():
    assert merge.merge_dict_value_list(
        {"a": [1, 2], "b": []}, {"a": [1, 3], "b": [5, 6]}
    ) == {"a": [1, 2, 1, 3], "b": [5, 6]}
    assert merge.merge_dict_value_list(
        {"a": [1, 2]}, {"a": [1, 3], "b": [5, 6]}
    ) == {"a": [1, 2, 1, 3], "b": [5, 6]}


def test_sum_values():
    assert (
        merge.sum_values(
            {1: 128, 2: 134, 3: 45, 4: 104, 5: 129},
            start=3,
            end=5,
        )
        == 278
    )


def test_add_list_value():
    assert merge.add_list_value({}, "test", "foo") == {"test": ["foo"]}
    assert merge.add_list_value({"test": ["bar"]}, "test", "foo") == {
        "test": ["bar", "foo"]
    }
