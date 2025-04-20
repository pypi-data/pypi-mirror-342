import re

from ddeutil.core import splitter as sp


def test_isplit():
    assert list(sp.isplit("abcb", "b")) == ["a", "c", ""]
    s = sp.isplit("foo bar")
    assert next(s) == "foo"
    assert next(s) == "bar"

    assert list(sp.isplit("ab||c||d", r"\|\|", regex=True)) == ["ab", "c", "d"]
    assert list(sp.isplit("ab||c||d", re.compile(r"\|\|"), regex=True)) == [
        "ab",
        "c",
        "d",
    ]
    assert list(sp.isplit("ab||c||d", regex=True)) == ["ab||c||d"]
    assert list(sp.isplit(b"ab c d")) == [b"ab", b"c", b"d"]


def test_must_split():
    assert sp.must_split("asd|foo", "|", maxsplit=2) == ["asd", "foo", None]
    assert sp.must_split("data") == ["data"]
    assert sp.must_split("data", "a", maxsplit=1, mustsplit=False) == [
        "d",
        "ta",
    ]

    assert sp.must_rsplit("asd|foo", "|", maxsplit=2) == [None, "asd", "foo"]
    assert sp.must_rsplit("foo bar", maxsplit=1) == ["foo", "bar"]
    assert sp.must_rsplit("foo") == ["foo"]


def test_rsplit():
    assert ["foo", "bar"] == sp.must_rsplit(
        "foo bar", maxsplit=2, mustsplit=False
    )
