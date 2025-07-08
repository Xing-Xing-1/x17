import pytest

from x17_container.dockers.base.resource import Resource


@pytest.fixture
def resource():
    """Fixture to create a Resource instance."""
    return Resource(name="test_resource", verbose=True)


def test_resource_initialization(resource):
    """Test the initialization of the Resource class."""
    assert resource.name == "test_resource"
    assert resource.verbose is True
    assert resource.type == "Resource"
    assert str(resource) == "test_resource"
    assert repr(resource) == "Resource(name=test_resource)"


def test_resource_default_initialization():
    """Test the default initialization of the Resource class."""
    resource = Resource()
    assert resource.name is None
    assert resource.verbose is False
    assert resource.type == "Resource"
    assert str(resource) == ""
    assert repr(resource) == "Resource(name=None)"


def test_resource_with_docker_client():
    """Test the Resource class with a Docker client."""
    from docker import from_env

    docker_client = from_env()
    resource = Resource(docker_client=docker_client, name="docker_resource")

    assert resource.docker_client is docker_client
    assert resource.name == "docker_resource"
    assert resource.type == "Resource"
    assert str(resource) == "docker_resource"
    assert repr(resource) == "Resource(name=docker_resource)"


def test_resource_logging():
    """Test the logging functionality of the Resource class."""
    resource = Resource(name="log_resource", verbose=True)
    assert resource.log_stream is not None
    assert resource.log_stream.name == "log_resource"
    assert resource.log_stream.verbose is True


def test_resource_repr():
    """Test the __repr__ method of the Resource class."""
    resource = Resource(name="repr_resource")
    assert repr(resource) == "Resource(name=repr_resource)"

    # Test with default name
    resource_default = Resource()
    assert repr(resource_default) == "Resource(name=None)"


def test_resource_str():
    """Test the __str__ method of the Resource class."""
    resource = Resource(name="str_resource")
    assert str(resource) == "str_resource"

    # Test with default name
    resource_default = Resource()
    assert str(resource_default) == ""


def test_resource_type():
    """Test the type property of the Resource class."""
    resource = Resource(name="type_resource")
    assert resource.type == "Resource"

    # Test with default initialization
    resource_default = Resource()
    assert resource_default.type == "Resource"


def test_resource_name():
    """Test the name property of the Resource class."""
    resource = Resource(name="name_resource")
    assert resource.name == "name_resource"

    # Test with default initialization
    resource_default = Resource()
    assert resource_default.name is None


def test_resource_verbose():
    """Test the verbose property of the Resource class."""
    resource = Resource(name="verbose_resource", verbose=True)
    assert resource.verbose is True

    # Test with default initialization
    resource_default = Resource()
    assert resource_default.verbose is False
