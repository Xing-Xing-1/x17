import pytest

from pangu.particle.datatype.semistruct import Semistruct


def test_initialization():
    s = Semistruct({"a": 1}, name="my-semistruct")
    assert s.name == "my-semistruct"
    assert s.get("a") == 1


def test_put_and_get():
    s = Semistruct()
    s.put("key", "value")
    assert s.get("key") == "value"
    assert s.get("nonexist", "default") == "default"


def test_remove_existing_key():
    s = Semistruct({"x": 42})
    s.remove("x")
    assert s.get("x") is None


def test_remove_nonexistent_key_does_not_fail():
    s = Semistruct()
    s.remove("missing")  # should not raise


def test_forbidden_getitem_warns():
    s = Semistruct({"a": 1})
    with pytest.warns(UserWarning, match=r"direct access obj\['a'\] is disabled"):
        _ = s["a"]


def test_forbidden_setitem_warns():
    s = Semistruct()
    with pytest.warns(
        UserWarning, match=r"direct assignment obj\['a'\] = 2 is disabled"
    ):
        s["a"] = 2


def test_update_warns():
    s = Semistruct()
    with pytest.warns(UserWarning, match="update\\(\\) is disabled"):
        s.update({"foo": "bar"})


def test_pop_warns():
    s = Semistruct({"key": "value"})
    with pytest.warns(UserWarning, match="pop\\(\\) is disabled"):
        s.pop("key")

def test_attr_returns_string_keys_only():
    s = Semistruct(name="test-name")
    s.non_string_attr = 123
    assert "name" in s.attr
    assert "non_string_attr" not in s.attr


def test_dict_returns_correct_mapping():
    s = Semistruct(name="semistruct-name")
    s.extra = "should-appear"
    s.non_string_attr = 456
    d = s.dict
    assert d == {"name": "semistruct-name", "extra": "should-appear"}


def test_repr_contains_class_name_and_attributes():
    s = Semistruct(name="myname")
    s.tag = "important"
    text = repr(s)
    assert "Semistruct" in text
    assert "name='myname'" in text
    assert "tag='important'" in text


def test_str_returns_name():
    s = Semistruct(name="visible-name")
    assert str(s) == "visible-name"


def test_str_returns_empty_if_name_none():
    s = Semistruct()
    assert str(s) == ""