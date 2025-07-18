from datetime import datetime

import pytest

from x17_container.dockers.base.structured import Structured


class Example(Structured):
    def __init__(
        self,
        name: str = "",
        age: int = 0,
        time: datetime = None,
    ):
        super().__init__(
            name=name,
            age=age,
            time=time or datetime.now(),
        )


def test_from_dict_and_to_dict():
    now = datetime(2025, 7, 18, 12, 0, 0)
    data = {"name": "Xing", "age": 26, "time": now}
    obj = Example.from_dict(data)

    assert isinstance(obj, Example)
    assert obj.name == "Xing"
    assert obj.age == 26
    assert isinstance(obj.time, datetime)

    dict_out = obj.to_dict()
    assert dict_out["name"] == "Xing"
    assert dict_out["age"] == 26
    assert dict_out["time"] == now.isoformat()


def test_get_method():
    obj = Example(name="Test", age=99)
    assert obj.get("name") == "Test"
    assert obj.get("missing", "default") == "default"


def test_equality_and_hash():
    now = datetime.now()
    a = Example(name="A", age=1, time=now)
    b = Example(name="A", age=1, time=now)
    c = Example(name="B", age=2, time=now)
    assert a == b
    assert a != c
    assert hash(a) == hash(b)
    assert hash(a) != hash(c)


def test_copy_with_override():
    now = datetime(2025, 1, 1)
    original = Example(name="X", age=30, time=now)
    clone = original.copy(name="Y")
    assert isinstance(clone, Example)
    assert clone.name == "Y"
    assert clone.age == 30
    assert clone.time == now
    assert original.name == "X"


def test_nested_structured():
    class Child(Structured):
        def __init__(self, label: str):
            super().__init__(label=label)

    class Parent(Structured):
        def __init__(self, child: Child):
            super().__init__(child=child)

    obj = Parent(child=Child("sub"))
    d = obj.to_dict()
    assert d["child"]["label"] == "sub"


def test_from_dict_and_to_dict():
    now = datetime(2025, 7, 18, 12, 0, 0)
    data = {"name": "Xing", "age": 26, "time": now}
    obj = Example.from_dict(data)

    assert isinstance(obj, Example)
    assert obj.name == "Xing"
    assert obj.age == 26
    assert isinstance(obj.time, datetime)

    dict_out = obj.to_dict()
    assert dict_out["name"] == "Xing"
    assert dict_out["age"] == 26
    assert dict_out["time"] == now.isoformat()


def test_copy_with_override():
    now = datetime(2025, 1, 1)
    original = Example(name="X", age=30, time=now)
    clone = original.copy(name="Y")

    assert isinstance(clone, Example)
    assert clone.name == "Y"
    assert clone.age == 30
    assert clone.time == now


def test_eq_and_ne():
    now = datetime(2025, 7, 18)
    a = Example(name="A", age=1, time=now)
    b = Example(name="A", age=1, time=now)
    c = Example(name="C", age=3, time=now)

    assert a == b
    assert a != c
    assert a != {"not": "structured"}


def test_nested_structured():
    class Inner(Structured):
        def __init__(self, value: int):
            super().__init__(value=value)

    class Outer(Structured):
        def __init__(self, inner: Inner):
            super().__init__(inner=inner)

    inner = Inner(value=42)
    outer = Outer(inner=inner)

    d = outer.to_dict()
    assert d["inner"]["value"] == 42


def test_list_of_structured():
    class Item(Structured):
        def __init__(self, id: int):
            super().__init__(id=id)

    class Container(Structured):
        def __init__(self, items: list[Item]):
            super().__init__(items=items)

    items = [Item(id=1), Item(id=2)]
    container = Container(items=items)

    d = container.to_dict()
    assert isinstance(d["items"], list)
    assert d["items"][0]["id"] == 1
    assert d["items"][1]["id"] == 2


def test_datetime_serialization():
    now = datetime(2025, 7, 18, 18, 0, 0)
    obj = Example(name="Test", age=10, time=now)
    d = obj.to_dict()
    assert d["time"] == now.isoformat()


def test_deserialization_with_datetime():
    now = datetime(2025, 7, 18, 18, 0, 0)
    data = {"name": "Test", "age": 10, "time": now.isoformat()}
    obj = Example.from_dict(data)

    assert isinstance(obj.time, str)
    assert obj.time == now.isoformat()
