from __future__ import absolute_import, division, print_function

import pytest

from symantecssl.datastructures import CaseInsensitiveDict


class TestCaseInsensitiveDict:

    @pytest.mark.parametrize(("initial", "expected"), [
        ({"a": "b"}, {"a": "b"}),
        (None, {}),
    ])
    def test_initial_data(self, initial, expected):
        assert CaseInsensitiveDict(initial) == expected

    def test_set_item(self):
        d = CaseInsensitiveDict()
        d["A"] = "one"
        d["a"] = "two"
        d["b"] = "three"

        assert d == {"a": "two", "b": "three"}

    def test_get_item(self):
        d = CaseInsensitiveDict({"a": "one"})

        assert d["a"] == "one"
        assert d["A"] == "one"

    def test_del_item(self):
        a = CaseInsensitiveDict({"a": "one"})
        b = CaseInsensitiveDict({"B": "two"})
        c = CaseInsensitiveDict({"c": "three"})

        del a["A"]
        del b["b"]
        del c["c"]

        assert "a" not in a
        assert "A" not in a
        assert "b" not in b
        assert "B" not in b
        assert "c" not in c
        assert "C" not in c

    def test_iter(self):
        assert set(CaseInsensitiveDict({"a": "", "B": ""})) == set(["a", "B"])

    def test_len(self):
        assert len(CaseInsensitiveDict()) == 0
        assert len(CaseInsensitiveDict({"a": None})) == 1
        assert len(CaseInsensitiveDict({"a": None, "b": None})) == 2

    def test_equality(self):
        # Empty
        assert CaseInsensitiveDict() == CaseInsensitiveDict()
        assert CaseInsensitiveDict() == {}
        assert {} == CaseInsensitiveDict()

        # Same cased items
        assert (
            CaseInsensitiveDict({"a": "one", "b": "two"})
            == CaseInsensitiveDict({"a": "one", "b": "two"})
        )
        assert (
            CaseInsensitiveDict({"a": "one", "b": "two"})
            == {"a": "one", "b": "two"}
        )
        assert (
            {"a": "one", "b": "two"}
            == CaseInsensitiveDict({"a": "one", "b": "two"})
        )

        # Differently cased items
        assert (
            CaseInsensitiveDict({"a": "one", "B": "two"})
            == CaseInsensitiveDict({"A": "one", "b": "two"})
        )
        assert (
            CaseInsensitiveDict({"a": "one", "B": "two"})
            == {"A": "one", "b": "two"}
        )
        assert (
            {"a": "one", "B": "two"}
            == CaseInsensitiveDict({"A": "one", "b": "two"})
        )

        # Nonsense
        assert CaseInsensitiveDict() != []

    def test_copy(self):
        a = CaseInsensitiveDict({"a": "one"})
        b = a.copy()

        a["b"] = "two"
        b["b"] = "three"

        assert a == {"a": "one", "b": "two"}
        assert b == {"a": "one", "b": "three"}

    def test_lower_items(self):
        d = CaseInsensitiveDict({"A": "one", "b": "two"})

        assert set(d.lower_items()) == set([("a", "one"), ("b", "two")])

    def test_repr(self):
        a = CaseInsensitiveDict({"A": "one"})
        b = CaseInsensitiveDict({"b": "one"})
        assert repr(a) == "CaseInsensitiveDict(%r)" % {"A": "one"}
        assert repr(b) == "CaseInsensitiveDict(%r)" % {"b": "one"}
