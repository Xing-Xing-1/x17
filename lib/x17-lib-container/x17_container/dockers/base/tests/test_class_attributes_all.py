from datetime import datetime

from x17_container.dockers.base.attributes import Attributes


class ExampleAttr(Attributes):
    def __init__(
        self,
        name: str = "",
        enabled: bool = True,
        timestamp: datetime = None,
    ):
        super().__init__(
            name=name,
            enabled=enabled,
            timestamp=timestamp or datetime(2025, 7, 18, 12, 0, 0),
        )


def test_attribute_from_dict_and_to_dict():
    now = datetime(2025, 7, 18, 12, 0, 0)
    data = {"name": "Alpha", "enabled": False, "timestamp": now}
    obj = ExampleAttr.from_dict(data)

    assert isinstance(obj, ExampleAttr)
    assert obj.name == "Alpha"
    assert obj.enabled is False
    assert obj.timestamp == now

    out = obj.to_dict()
    assert out["name"] == "Alpha"
    assert out["enabled"] is False
    assert out["timestamp"] == now.isoformat()


def test_attribute_equality_and_hash():
    now = datetime(2025, 7, 18, 12, 0, 0)
    a1 = ExampleAttr(name="Same", enabled=True, timestamp=now)
    a2 = ExampleAttr(name="Same", enabled=True, timestamp=now)

    assert a1 == a2
    assert hash(a1) == hash(a2)


def test_attribute_copy_with_override():
    now = datetime(2025, 7, 18, 12, 0, 0)
    original = ExampleAttr(name="X", enabled=True, timestamp=now)
    clone = original.copy(name="Y")

    assert isinstance(clone, ExampleAttr)
    assert clone.name == "Y"
    assert clone.enabled is True
    assert clone.timestamp == now


def test_attribute_nested_dict():
    class WithNested(Attributes):
        def __init__(self, inner: dict = None):
            super().__init__(inner=inner or {"keyA": 123, "keyB": "abc"})

    obj = WithNested()
    d = obj.to_dict()
    assert d["inner"]["keyA"] == 123
    assert d["inner"]["keyB"] == "abc"


def test_attribute_describe():
    now = datetime(2025, 7, 18, 12, 0, 0)
    attr = ExampleAttr(name="Test", enabled=True, timestamp=now)
    description = attr.describe()

    assert description["name"] == "Test"
    assert description["enabled"] is True
    assert description["timestamp"] == now.isoformat()


class ComplexAttr(Attributes):
    def __init__(
        self,
        tags: list[str] = None,
        metadata: dict = None,
        created: datetime = None,
    ):
        super().__init__(
            tags=tags or ["docker", "test"],
            metadata=metadata or {"version": "1.0", "author": "x"},
            created=created or datetime(2025, 7, 18, 12, 0, 0),
        )


def test_attribute_with_list_and_dict():
    obj = ComplexAttr()
    d = obj.to_dict()

    assert isinstance(d["tags"], list)
    assert "docker" in d["tags"]
    assert d["metadata"]["version"] == "1.0"
    assert isinstance(d["created"], str)  # datetime serialized


def test_attribute_empty_fields():
    class EmptyAttr(Attributes):
        def __init__(self):
            super().__init__()

    obj = EmptyAttr()
    d = obj.to_dict()
    assert isinstance(d, dict)
    assert d == {}


def test_attribute_non_serializable_field():
    class NonSerializable(Attributes):
        def __init__(self, obj=None):
            super().__init__(obj=obj or set([1, 2, 3]))  # set is not JSON serializable

    obj = NonSerializable()
    d = obj.to_dict()
    assert isinstance(
        d["obj"], set
    )  # it remains a set, caller must handle serialization


def test_attribute_nested_structured():
    class Inner(Attributes):
        def __init__(self, value: int = 0):
            super().__init__(value=value)

    class Outer(Attributes):
        def __init__(self, inner: Inner = None):
            super().__init__(inner=inner or Inner(42))

    obj = Outer()
    d = obj.to_dict()
    assert isinstance(d["inner"], dict)
    assert d["inner"]["value"] == 42


def test_attribute_equality_against_dict():
    obj = ComplexAttr(
        tags=["a", "b"], metadata={"k": "v"}, created=datetime(2025, 7, 18, 12, 0, 0)
    )
    dict_like = {
        "tags": ["a", "b"],
        "metadata": {"k": "v"},
        "created": "2025-07-18T12:00:00",
    }
    assert obj == dict_like
