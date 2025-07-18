from datetime import datetime

from x17_container.dockers.base.configuration import Configuration


class ExampleConfig(Configuration):

    def __init__(
        self,
        name: str = "",
        enabled: bool = True,
        timestamp: datetime = None,
        metadata: dict = None,
        tags: list = None,
    ):
        super().__init__(
            name=name,
            enabled=enabled,
            timestamp=timestamp or datetime(2025, 7, 18, 12, 0, 0),
            metadata=metadata or {},
            tags=tags or [],
        )


def test_configuration_basic():
    now = datetime(2025, 7, 18, 12, 0, 0)
    config = ExampleConfig(name="test", enabled=False, timestamp=now)

    assert config.name == "test"
    assert config.enabled is False
    assert config.timestamp == now


def test_configuration_to_dict_and_from_dict():
    now = datetime(2025, 7, 18, 12, 0, 0)
    data = {
        "name": "config-x",
        "enabled": True,
        "timestamp": now,
    }
    config = ExampleConfig.from_dict(data)
    assert config.name == "config-x"
    assert config.enabled is True
    assert config.timestamp == now

    dict_out = config.to_dict()
    assert dict_out["name"] == "config-x"
    assert dict_out["enabled"] is True
    assert dict_out["timestamp"] == now.isoformat()


def test_configuration_copy():
    config = ExampleConfig(name="copyme", enabled=True)
    copied = config.copy(name="copied")

    assert copied.name == "copied"
    assert copied.enabled is True
    assert isinstance(copied, ExampleConfig)


def test_configuration_eq_and_hash():
    now = datetime(2025, 7, 18, 12, 0, 0)
    config1 = ExampleConfig(name="a", timestamp=now)
    config2 = ExampleConfig(name="a", timestamp=now)

    assert config1 == config2
    assert hash(config1) == hash(config2)

    config3 = ExampleConfig(name="b", timestamp=now)
    assert config1 != config3


def test_configuration_describe():
    config = ExampleConfig(name="alpha", enabled=False)
    desc = config.describe()

    assert isinstance(desc, dict)
    assert desc["name"] == "alpha"
    assert desc["enabled"] is False

    filtered = config.describe(fields=["name"])
    assert filtered == {"name": "alpha"}


def test_basic_to_dict_and_from_dict():
    now = datetime(2025, 7, 18, 12, 0, 0)
    data = {
        "name": "test",
        "enabled": False,
        "timestamp": now,
        "metadata": {"env": "dev"},
        "tags": ["docker", "test"],
    }

    obj = ExampleConfig.from_dict(data)
    assert isinstance(obj, ExampleConfig)
    assert obj.name == "test"
    assert obj.enabled is False
    assert obj.timestamp == now
    assert obj.metadata == {"env": "dev"}
    assert obj.tags == ["docker", "test"]

    output = obj.to_dict()
    assert output["timestamp"] == now.isoformat()
    assert output["metadata"]["env"] == "dev"


def test_empty_configuration():
    obj = ExampleConfig()
    output = obj.to_dict()
    assert output["name"] == ""
    assert output["enabled"] is True
    assert isinstance(output["timestamp"], str)
    assert output["metadata"] == {}
    assert output["tags"] == []


def test_nested_dict_and_list_serialization():
    now = datetime(2025, 7, 18, 12, 0, 0)
    obj = ExampleConfig(
        name="complex",
        metadata={"env": "prod", "version": {"major": 1, "minor": 0}},
        tags=["x17", {"label": "core"}],
        timestamp=now,
    )
    result = obj.to_dict()
    assert result["metadata"]["version"]["major"] == 1
    assert isinstance(result["timestamp"], str)
    assert result["tags"][1]["label"] == "core"


def test_partial_overrides_copy():
    now = datetime(2025, 7, 18, 12, 0, 0)
    obj = ExampleConfig(name="base", timestamp=now)
    copied = obj.copy(enabled=False, name="override")
    assert copied.name == "override"
    assert copied.enabled is False
    assert copied.timestamp == now


def test_invalid_field_access_returns_default():
    obj = ExampleConfig(name="abc")
    assert obj.get("non_existent", default="fallback") == "fallback"
    assert obj.get("name") == "abc"
