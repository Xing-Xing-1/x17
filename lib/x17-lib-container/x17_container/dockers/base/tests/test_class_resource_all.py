from unittest.mock import MagicMock

import pytest

from x17_container.dockers.base.attributes import Attributes
from x17_container.dockers.base.configuration import Configuration
from x17_container.dockers.base.resource import Resource


@pytest.fixture
def config_dict():
    return {"name": "test-resource", "driver": "bridge"}


@pytest.fixture
def attr_dict():
    return {"id": "abc123", "status": "running"}


@pytest.fixture
def config_obj():
    return Configuration(name="obj-resource", driver="host")


@pytest.fixture
def attr_obj():
    return Attributes(id="def456", status="exited")


def test_init_with_dicts(config_dict, attr_dict):
    resource = Resource(configuration=config_dict, attributes=attr_dict, verbose=True)
    assert resource.configuration.name == "test-resource"
    assert resource.configuration.driver == "bridge"
    assert resource.attributes.id == "abc123"
    assert resource.attributes.status == "running"
    assert "test-resource" in str(resource)
    assert "Resource(name=test-resource" in repr(resource)


def test_init_with_objects(config_obj, attr_obj):
    resource = Resource(configuration=config_obj, attributes=attr_obj)
    assert resource.name == "obj-resource"
    assert resource.configuration.driver == "host"
    assert resource.attributes.status == "exited"


def test_fallback_name():
    resource = Resource()
    assert resource.name.startswith("Resource-")


def test_describe_output(config_dict, attr_dict):
    resource = Resource(configuration=config_dict, attributes=attr_dict)
    desc = resource.describe()
    assert desc["name"] == "test-resource"
    assert desc["type"] == "Resource"
    assert desc["configuration"]["driver"] == "bridge"
    assert desc["attributes"]["status"] == "running"


def test_interface_methods_exist():
    resource = Resource()
    assert hasattr(resource, "create") and callable(resource.create)
    assert hasattr(resource, "remove") and callable(resource.remove)
    assert hasattr(resource, "load") and callable(resource.load)
    assert hasattr(resource, "exists") and callable(resource.exists)


def test_name_from_configuration():
    conf = Configuration(name="net-conf")
    attr = Attributes(name="net-attr")
    res = Resource(configuration=conf, attributes=attr)
    assert res.name == "net-conf"


def test_name_from_attributes_if_no_configuration_name():
    conf = Configuration()
    attr = Attributes(name="net-attr")
    res = Resource(configuration=conf, attributes=attr)
    assert res.name == "net-attr"


def test_name_generated_if_none_provided():
    res = Resource(configuration={}, attributes={})
    assert res.name.startswith("Resource-")
    assert len(res.name) > len("Resource-")


def test_str_and_repr_are_correct():
    conf = Configuration(name="hello-net")
    res = Resource(configuration=conf)
    assert str(res) == "hello-net"
    assert repr(res) == "Resource(name=hello-net)"


def test_describe_output_structure():
    conf = Configuration(name="net1", driver="bridge")
    attr = Attributes(id="abc123", driver="bridge")
    res = Resource(configuration=conf, attributes=attr)
    desc = res.describe()

    assert desc["name"] == "net1"
    assert desc["type"] == "Resource"
    assert desc["configuration"]["driver"] == "bridge"
    assert desc["attributes"]["id"] == "abc123"


def test_each_resource_gets_unique_physical_id():
    r1 = Resource(configuration={})
    r2 = Resource(configuration={})
    assert r1.physical_id != r2.physical_id


def test_log_stream_name_matches_resource_name():
    res = Resource(configuration={"name": "streamy"})
    assert res.log_stream.name == "streamy"


def test_can_inject_custom_docker_client():
    fake_client = MagicMock()
    res = Resource(configuration={}, docker_client=fake_client)
    assert res.docker_client is fake_client


def test_resource_name_and_type():
    conf = Configuration(name="my-resource")
    res = Resource(configuration=conf)

    assert res.name == "my-resource"
    assert res.type == "Resource"
    assert str(res) == "my-resource"
    assert repr(res) == "Resource(name=my-resource)"


def test_resource_auto_name_from_attribute():
    attr = Attributes(name="attr-name")
    res = Resource(attributes=attr)

    assert res.name == "attr-name"
    assert "attr-name" in str(res)


def test_resource_name_fallback():
    res = Resource()
    assert res.name.startswith("Resource-")
    assert res.name == str(res)


def test_resource_describe_basic():
    conf = Configuration(name="conf-name", enabled=True)
    attr = Attributes(foo="bar")
    res = Resource(configuration=conf, attributes=attr)

    desc = res.describe()
    assert desc["name"] == "conf-name"
    assert desc["type"] == "Resource"
    assert desc["configuration"]["name"] == "conf-name"
    assert desc["attributes"]["foo"] == "bar"


def test_resource_children_management():
    parent = Resource(configuration=Configuration(name="parent"))
    child = Resource(configuration=Configuration(name="child"))

    parent.add_child(child)
    assert "child" in parent.children
    assert parent.get_child("child") is child

    parent.remove_child(child)
    assert "child" not in parent.children


def test_resource_describe_with_children():
    parent = Resource(configuration=Configuration(name="p"))
    child1 = Resource(configuration=Configuration(name="c1"))
    child2 = Resource(configuration=Configuration(name="c2"))

    parent.add_child(child1)
    parent.add_child(child2)

    desc = parent.describe(include_children=True)
    assert "children" in desc
    assert "c1" in desc["children"]
    assert desc["children"]["c1"]["name"] == "c1"
    assert desc["children"]["c2"]["type"] == "Resource"


def test_resource_accepts_dict_input():
    res = Resource(
        configuration={"name": "dict-conf"},
        attributes={"env": "dev"},
    )
    assert res.configuration.name == "dict-conf"
    assert res.attributes.env == "dev"


def test_resource_describe_without_config_or_attr():
    res = Resource()
    desc = res.describe()
    assert "name" in desc
    assert isinstance(desc["configuration"], dict)
    assert isinstance(desc["attributes"], dict)


def test_resource_add_child_overwrite():
    parent = Resource(configuration={"name": "parent"})
    child1 = Resource(configuration={"name": "child"})
    child2 = Resource(configuration={"name": "child"})  # same name

    parent.add_child(child1)
    parent.add_child(child2)

    assert len(parent.children) == 1
    assert parent.get_child("child") is child2


def test_remove_child_safely_handles_missing():
    parent = Resource(configuration={"name": "p"})
    ghost = Resource(configuration={"name": "ghost"})

    parent.remove_child(ghost)  # should not raise
    assert "ghost" not in parent.children


def test_resource_physical_id_uniqueness():
    r1 = Resource()
    r2 = Resource()
    assert r1.name != r2.name
