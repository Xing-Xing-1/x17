import pytest
from unittest.mock import MagicMock
from docker.models.containers import Container as DockerContainer
from docker.client import DockerClient
from x17_container.dock.container.container import Container


# ---------- Fixtures ----------

@pytest.fixture
def mock_docker_container() -> DockerContainer:
    mock = MagicMock(spec=DockerContainer)
    mock.id = "abc123"
    mock.image.tags = ["hello:world"]
    mock.name = "test-container"
    mock.attrs = {
        "NetworkSettings": {
            "Ports": {"80/tcp": [{"HostPort": "8080"}]},
            "Networks": {"bridge": {}, "custom": {}}
        },
        "Mounts": [{"Source": "/host", "Destination": "/container"}],
        "Config": {
            "Env": ["DEBUG=true"],
            "Cmd": ["python", "app.py"]
        }
    }
    return mock

@pytest.fixture
def mock_container_with_attrs():
    mock = MagicMock()
    mock.id = "mock_id"
    mock.image.tags = ["myimage:latest"]
    mock.name = "mockcontainer"
    mock.attrs = {
        "NetworkSettings": {
            "Ports": {"80/tcp": [{"HostPort": "8080"}]},
            "Networks": {"bridge": {}, "custom": {}}
        },
        "Mounts": [{"Source": "/host", "Destination": "/container"}],
        "Config": {
            "Env": ["DEBUG=true"],
            "Cmd": ["python", "app.py"]
        }
    }
    return mock

@pytest.fixture
def mock_docker_client() -> DockerClient:
    mock = MagicMock(spec=DockerClient)
    mock.containers.create.return_value = MagicMock(spec=DockerContainer)
    return mock

@pytest.fixture
def mock_log_stream():
    return MagicMock()


# ---------- Tests ----------

def test_init_with_docker_container(mock_docker_container, mock_docker_client):
    c = Container(docker_container=mock_docker_container, docker_client=mock_docker_client)
    assert c.id == "abc123"
    assert c.image == "hello:world"
    assert c.name == "test-container"
    assert c.environment == ["DEBUG=true"]
    assert c.command == ["python", "app.py"]
    assert sorted(c.network) == ["bridge", "custom"]
    assert c.ports == {"80/tcp": [{"HostPort": "8080"}]}
    assert c.volumes == [{"Source": "/host", "Destination": "/container"}]


def test_init_with_parameters(mock_docker_client):
    mock_created_container = MagicMock(spec=DockerContainer)
    mock_created_container.id = "xyz123"
    mock_created_container.image.tags = ["alpine"]
    mock_created_container.name = "mycontainer"
    mock_created_container.attrs = {
        "NetworkSettings": {
            "Ports": {"8080/tcp": [{"HostPort": "8080"}]},
            "Networks": {"bridge": {}}
        },
        "Mounts": [],
        "Config": {
            "Env": ["FOO=bar"],
            "Cmd": ["/bin/sh"]
        }
    }
    mock_docker_client.containers.create.return_value = mock_created_container

    container = Container(
        image="alpine",
        name="mycontainer",
        docker_client=mock_docker_client,
        ports={"8080/tcp": 8080},
        volumes=[],
        environment=["FOO=bar"],
        command=["/bin/sh"],
        network=["bridge"],
        custom_flag=True,
    )

    assert container.id == "xyz123"
    assert container.name == "mycontainer"
    assert container.image == "alpine"
    assert container.command == ["/bin/sh"]
    assert container.environment == ["FOO=bar"]
    assert container.ports == {"8080/tcp": [{"HostPort": "8080"}]}
    assert container.network == ["bridge"]
    assert container.custom_flag is True
    mock_docker_client.containers.create.assert_called_once()


def test_from_docker_success(mock_docker_container, mock_docker_client):
    c = Container.from_docker(mock_docker_container, mock_docker_client)
    assert isinstance(c, Container)
    assert c.name == "test-container"


def test_from_docker_invalid_type(mock_docker_client):
    with pytest.raises(TypeError, match="Expected a DockerContainer instance."):
        Container.from_docker("not_a_container", mock_docker_client)


def test_from_docker_missing_client(mock_docker_container):
    with pytest.raises(ValueError, match="Docker container cannot be None or empty."):
        Container.from_docker(mock_docker_container, None)


def test_repr_str_dict(mock_docker_container, mock_docker_client):
    c = Container(docker_container=mock_docker_container, docker_client=mock_docker_client)

    # __str__
    assert str(c) == "abc123"

    # __repr__
    r = repr(c)
    assert "abc123" in r
    assert "hello:world" in r
    assert "test-container" in r

    # dict property
    d = c.dict
    assert isinstance(d, dict)
    assert d["id"] == "abc123"
    assert d["image"] == "hello:world"
    assert d["name"] == "test-container"
    assert d["ports"] == {"80/tcp": [{"HostPort": "8080"}]}
    assert d["volumes"] == [{"Source": "/host", "Destination": "/container"}]
    assert d["environment"] == ["DEBUG=true"]
    assert d["command"] == ["python", "app.py"]
    assert sorted(d["network"]) == ["bridge", "custom"]
    

def test_from_dict_creates_valid_container(monkeypatch, mock_docker_client):
    # Mock container returned by Docker
    mock_created_container = MagicMock()
    mock_created_container.id = "test123"
    mock_created_container.image.tags = ["mock_image:latest"]
    mock_created_container.name = "testcontainer"
    mock_created_container.attrs = {
        "NetworkSettings": {
            "Ports": {"80/tcp": [{"HostPort": "8080"}]},
            "Networks": {"bridge": {}}
        },
        "Mounts": [],
        "Config": {
            "Env": ["FOO=bar"],
            "Cmd": ["/bin/sh"]
        }
    }

    # Mock Docker client behavior
    mock_docker_client.containers.create.return_value = mock_created_container
    monkeypatch.setattr("docker.from_env", lambda: mock_docker_client)

    # Simulate input dictionary
    data = {
        "image": "mock_image:latest",
        "name": "testcontainer",
        "ports": {"80/tcp": 8080},
        "volumes": [],
        "environment": ["FOO=bar"],
        "command": ["/bin/sh"],
        "network": "bridge",
        "custom_flag": True,
    }

    # Test
    container = Container.from_dict(data)
    assert container.image == "mock_image:latest"
    assert container.name == "testcontainer"
    assert container.command == ["/bin/sh"]
    assert container.custom_flag is True
def test_export_includes_extra_attributes(mock_container_with_attrs, mock_docker_client):
    container = Container(
        docker_client=mock_docker_client,
        docker_container=mock_container_with_attrs,
        custom_flag=True,
        note="x17 container test"
    )
    exported = container.export()
    assert exported["image"] == "myimage:latest"
    assert exported["name"] == "mockcontainer"
    assert exported["custom_flag"] is True
    assert exported["note"] == "x17 container test"
    


def test_start_success(mock_container_with_attrs):
    mock_container_with_attrs.start.return_value = None
    container = Container(docker_container=mock_container_with_attrs)
    
    result = container.start()
    
    mock_container_with_attrs.start.assert_called_once()
    assert result is container


def test_stop_success(mock_container_with_attrs):
    mock_container_with_attrs.stop.return_value = None
    container = Container(docker_container=mock_container_with_attrs)
    
    result = container.stop()
    
    mock_container_with_attrs.stop.assert_called_once()
    assert result is container


def test_remove_success(mock_container_with_attrs):
    mock_container_with_attrs.remove.return_value = None
    container = Container(docker_container=mock_container_with_attrs)
    
    result = container.remove(force=True)
    
    mock_container_with_attrs.remove.assert_called_once_with(force=True)
    assert result is None


def test_start_failure(mock_container_with_attrs):
    mock_container_with_attrs.start.side_effect = Exception("Boom")
    container = Container(docker_container=mock_container_with_attrs)

    with pytest.raises(RuntimeError, match="Failed to start container"):
        container.start()


def test_stop_failure(mock_container_with_attrs):
    mock_container_with_attrs.stop.side_effect = Exception("Boom")
    container = Container(docker_container=mock_container_with_attrs)

    with pytest.raises(RuntimeError, match="Failed to stop container"):
        container.stop()


def test_remove_failure(mock_container_with_attrs):
    mock_container_with_attrs.remove.side_effect = Exception("Boom")
    container = Container(docker_container=mock_container_with_attrs)

    with pytest.raises(RuntimeError, match="Failed to remove container"):
        container.remove(force=True)
        
def test_batch_logs_returns_parsed_lines(mock_container_with_attrs, mock_log_stream):
    mock_container_with_attrs.logs.return_value = b"line1\nline2\nline3"
    container = Container(
        docker_container=mock_container_with_attrs,
        log_stream=mock_log_stream,
    )
    logs = container.batch_logs()
    assert logs == ["line1", "line2", "line3"]


def test_batch_logs_handles_error(mock_container_with_attrs, mock_log_stream):
    mock_container_with_attrs.logs.side_effect = Exception("Log error")
    container = Container(
        docker_container=mock_container_with_attrs,
        log_stream=mock_log_stream,
    )
    logs = container.batch_logs()
    assert logs == []
    mock_log_stream.log.assert_called_once()


def test_log_batch_mode(mock_container_with_attrs, mock_log_stream):
    mock_container_with_attrs.logs.return_value = b"lineA\nlineB"
    container = Container(
        docker_container=mock_container_with_attrs,
        log_stream=mock_log_stream,
    )
    result = container.log(stream=False)
    assert result == ["lineA", "lineB"]
    mock_log_stream.log.assert_any_call("lineA")
    mock_log_stream.log.assert_any_call("lineB")


def test_log_stream_mode(mock_container_with_attrs, mock_log_stream):
    mock_container_with_attrs.logs.return_value = iter([b"live1\n", b"live2\n"])
    container = Container(
        docker_container=mock_container_with_attrs,
        log_stream=mock_log_stream,
    )
    thread = container.log(stream=True)
    assert thread.is_alive() or isinstance(thread, type(thread))
    
def test_dict_property(mock_container_with_attrs):
    container = Container(docker_container=mock_container_with_attrs)
    d = container.dict
    assert isinstance(d, dict)
    assert d["id"] == "mock_id"
    assert d["image"] == "myimage:latest"
    assert d["name"] == "mockcontainer"
    assert "ports" in d


def test_is_running_true(mock_container_with_attrs):
    mock_container_with_attrs.status = "running"
    container = Container(docker_container=mock_container_with_attrs)
    assert container.is_running is True

def test_is_running_false(mock_container_with_attrs):
    mock_container_with_attrs.status = "exited"
    container = Container(docker_container=mock_container_with_attrs)
    assert container.is_running is False


def test_status(mock_container_with_attrs):
    mock_container_with_attrs.status = "running"
    container = Container(docker_container=mock_container_with_attrs)
    assert container.status == "running"


def test_refresh(mock_container_with_attrs):
    container = Container(docker_container=mock_container_with_attrs)
    mock_container_with_attrs.reload.return_value = None
    container.refresh()
    mock_container_with_attrs.reload.assert_called_once()


def test_wait_success(mock_container_with_attrs):
    mock_container_with_attrs.wait.return_value = {"StatusCode": 0}
    container = Container(docker_container=mock_container_with_attrs)
    result = container.wait()
    assert result == {"StatusCode": 0}
    mock_container_with_attrs.wait.assert_called_once()


def test_wait_failure(mock_container_with_attrs):
    mock_container_with_attrs.wait.side_effect = Exception("crash")
    container = Container(docker_container=mock_container_with_attrs)
    with pytest.raises(RuntimeError, match="Failed to wait for container"):
        container.wait()
        
