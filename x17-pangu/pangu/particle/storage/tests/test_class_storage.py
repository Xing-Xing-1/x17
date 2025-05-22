# -*- coding: utf-8 -*-
import pytest
from pangu.particle.storage.storage import Storage


def test_init_and_dict():
    s = Storage(100, "kb")
    assert s.size == 100
    assert s.unit == "kb"
    assert s.dict["unit"] == "kb"


def test_get_base():
    s = Storage(1, "kb")
    assert s.get_base() == 1024.0


def test_repr_and_str():
    s = Storage(5, "mb")
    assert "5" in repr(s)
    assert "mb" in str(s)


def test_add_storage():
    s1 = Storage(1, "kb")
    s2 = Storage(1, "kb")
    result = s1 + s2
    assert result.unit == "kb"
    assert result.size == 2


def test_add_number():
    s = Storage(10, "mb")
    result = s + 5
    assert result.size == 15
    assert result.unit == "mb"


def test_sub_storage():
    s1 = Storage(2, "gb")
    s2 = Storage(1, "gb")
    result = s1 - s2
    assert result.unit == "gb"
    assert result.size == 1


def test_sub_number():
    s = Storage(10, "mb")
    result = s - 3
    assert result.size == 7
    assert result.unit == "mb"


def test_mul():
    s = Storage(2, "mb")
    result = s * 3
    assert result.size == 6
    assert result.unit == "mb"


def test_eq_storage():
    s1 = Storage(1, "gb")
    s2 = Storage(1024, "mb")
    assert s1 == s2


def test_eq_number():
    s = Storage(10, "mb")
    assert s == 10


def test_to_unit():
    s = Storage(1, "gb")
    converted = s.to_unit("mb")
    assert converted.unit == "mb"
    assert pytest.approx(converted.size, 0.01) == 1024


def test_as_unit_chainable():
    s = Storage(2048, "kb")
    s.as_unit("mb")
    assert s.unit == "mb"
    assert pytest.approx(s.size, 0.01) == 2


def test_get_readable_unit():
    s = Storage(2048, "kb")
    assert s.get_readable_unit() == "mb"


def test_to_readable_conversion():
    s = Storage(1536, "kb")
    r = s.to_readable()
    assert isinstance(r, Storage)
    assert r.unit == "mb"
    assert pytest.approx(r.size, 0.01) == 1.5


def test_as_readable_chainable():
    s = Storage(2048, "kb")
    s.as_readable()
    assert s.unit == "mb"
    assert pytest.approx(s.size, 0.01) == 2


def test_export():
    s = Storage(100, "kb")
    exported = s.export()
    assert exported["size"] == 100
    assert exported["unit"] == "kb"