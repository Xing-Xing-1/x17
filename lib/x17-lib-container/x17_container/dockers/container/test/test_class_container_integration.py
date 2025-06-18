import pytest
import docker
import time
from x17_container.dockers.container.container import Container

#@pytest.mark.integration
def test_container_lifecycle_integration():
    image = "alpine:latest"
    name = "x17-test-container"
    command = ["echo", "Hello, x17"]
    
    client = docker.from_env()
    try:
        existing = client.containers.get(name)
        existing.remove(force=True)
    except docker.errors.NotFound:
        pass

    container = Container(
        image=image,
        name=name,
        command=command,
        auto_remove=False,
        detach=True,
        verbose=True,
    )

    container.start()
    assert container.status in ("created", "running", "exited")

    result = container.wait()
    assert result["StatusCode"] == 0

    logs = container.batch_logs()
    assert any("Hello, x17" in log for log in logs)

    try:
        container.remove(force=True)
    except Exception:
        pass
    
    
#@pytest.mark.integration
def test_container_lifecycle_echo():
    image = "alpine:latest"
    name = "x17-test-echo"
    command = ["echo", "Integration test success!"]

    client = docker.from_env()
    try:
        client.containers.get(name).remove(force=True)
    except docker.errors.NotFound:
        pass

    container = Container(
        image=image,
        name=name,
        command=command,
        auto_remove=False,
        detach=True,
        verbose=True,
    )

    container.start()
    result = container.wait()
    assert result["StatusCode"] == 0

    logs = container.batch_logs()
    assert any("Integration test success!" in log for log in logs)

    container.remove(force=True)
    
#@pytest.mark.integration
def test_container_with_ports():
    image = "nginx:latest"
    name = "x17-test-nginx"
    ports = {"80/tcp": ("127.0.0.1", 8081)}

    client = docker.from_env()
    try:
        client.containers.get(name).remove(force=True)
    except docker.errors.NotFound:
        pass

    container = Container(
        image=image,
        name=name,
        ports=ports,
        auto_remove=False,
        detach=True,
        verbose=True,
    )

    container.start()
    for _ in range(5):
        container.refresh()
        ports = container.ports
        if "80/tcp" in ports:
            break
        time.sleep(2)
    print(container.docker_container.attrs["HostConfig"]["PortBindings"])
    print(container.docker_container.attrs["NetworkSettings"]["Ports"])
    assert "80/tcp" in ports
    assert ports["80/tcp"][0]["HostPort"] == "8081"

    container.stop()
    container.remove(force=True)
    
#@pytest.mark.integration
def test_container_with_env_vars():
    image = "alpine:latest"
    name = "x17-test-env"
    command = ["sh", "-c", "echo $TEST_KEY"]
    environment = ["TEST_KEY=VALUE_123"]

    client = docker.from_env()
    try:
        client.containers.get(name).remove(force=True)
    except docker.errors.NotFound:
        pass

    container = Container(
        image=image,
        name=name,
        command=command,
        environment=environment,
        auto_remove=False,
        detach=True,
        verbose=True,
    )

    container.start()
    result = container.wait()
    assert result["StatusCode"] == 0

    logs = container.batch_logs()
    assert any("VALUE_123" in log for log in logs)

    container.remove(force=True)
    
#@pytest.mark.integration
def test_container_pull_failure_handling():
    image = "this_image_should_not_exist:v1"

    with pytest.raises(RuntimeError) as exc_info:
        Container(
            image=image,
            name="x17-test-fail",
            auto_remove=True,
            detach=True,
            verbose=True,
        )

    assert "Failed to pull image" in str(exc_info.value)
    
