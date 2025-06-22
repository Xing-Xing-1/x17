import os
import shutil
import pytest
from pathlib import Path
from x17_container.dockers.mount.host import MountHost

@pytest.fixture
def temp_dir(tmp_path):
    yield tmp_path
    if tmp_path.exists():
        shutil.rmtree(tmp_path)

@pytest.fixture
def mount_host(temp_dir):
    return MountHost(
        mountpoint=temp_dir / "host_dir",
        target="/data",  # Simulated container path
        name="x17_test_bind_mount",
        mode="rw",
        chmod=True,
        permission={"uid": 1000, "gid": 1000, "mode": 0o755},
        verbose=True,
    )

def test_mounthost_create_and_exists(mount_host):
    assert not mount_host.exists()
    mount_host.create()
    assert mount_host.exists()

def test_mounthost_chmod_permission_scripts(mount_host):
    mount_host.create()
    assert "chown" in mount_host.permission_script
    assert mount_host.chmod_script is None

def test_mounthost_dict_content(mount_host):
    mount_host.create()
    data = mount_host.dict
    assert data["name"] == "x17_test_bind_mount"
    assert data["mode"] == "rw"
    assert "mountpoint" in data
    assert data["permission"]["uid"] == 1000

def test_mounthost_docker_bind_format(mount_host):
    docker_bind = mount_host.to_docker_host()
    key = str(mount_host.mountpoint)
    assert key in docker_bind
    assert docker_bind[key]["bind"] == str(mount_host.target)
    assert docker_bind[key]["mode"] == "rw"

def test_mounthost_str_repr_eq(mount_host):
    other = MountHost(
        mountpoint=mount_host.mountpoint,
        target=mount_host.target,
        mode=mount_host.mode,
    )
    assert str(mount_host) == f"{mount_host.mountpoint} -> {mount_host.target}"
    assert repr(mount_host).startswith("MountHost(")
    assert mount_host == other
    assert not (mount_host != other)

def test_mounthost_delete(mount_host):
    mount_host.create()
    assert mount_host.exists()
    mount_host.delete()
    assert not mount_host.exists()
    
# -- Test setup for MountHost class --
    
BASE_PATH = Path("/tmp/x17-test-host")
HOST_PATH = BASE_PATH / "bind_mount_dir"

@pytest.fixture(scope="module")
def mount_base_path():
    if BASE_PATH.exists():
        shutil.rmtree(BASE_PATH, ignore_errors=True)
    BASE_PATH.mkdir(parents=True, exist_ok=True)
    yield BASE_PATH
    if BASE_PATH.exists():
        shutil.rmtree(BASE_PATH, ignore_errors=True)

@pytest.fixture
def mount_host(mount_base_path):
    host_path = mount_base_path / "bind_mount_dir"
    if host_path.exists():
        shutil.rmtree(host_path, ignore_errors=True)

    m = MountHost(
        mountpoint=host_path,
        target="/app/data",
        name="x17_test_bind_mount",
        mode="rw",
        chmod=True,
        permission={"uid": 1000, "gid": 1000, "mode": 0o755},
        verbose=True,
    )
    yield m

    if host_path.exists():
        shutil.rmtree(host_path, ignore_errors=True)
        
def test_create_and_check_exists(mount_host):
    mount_host.create()
    assert mount_host.exists()
    assert mount_host.mountpoint.exists()

def test_force_create_and_delete(mount_host):
    mount_host.create()
    assert mount_host.mountpoint.exists()
    mount_host.create(force=True)
    assert mount_host.mountpoint.exists()
    mount_host.delete()
    assert not mount_host.mountpoint.exists()

def test_permission_script_content(mount_host):
    mount_host.create()
    script = mount_host.permission_script
    assert "chown" in script
    assert "chmod" in script
    assert str(mount_host.mountpoint) in script

def test_docker_bind_format(mount_host):
    bind = mount_host.to_docker_host()
    assert str(mount_host.mountpoint) in bind
    entry = bind[str(mount_host.mountpoint)]
    assert entry["bind"] == str(mount_host.target)
    assert entry["mode"] == "rw"

def test_from_dict_behavior(mount_base_path):
    path = mount_base_path / "dict_bind_dir"
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)

    config = {
        "mountpoint": str(path),
        "target": "/app/data",
        "name": "dict_test_bind",
        "mode": "ro",
        "chmod": True,
        "permission": {"uid": 2000, "gid": 2000, "mode": 0o700},
    }
    m = MountHost.from_dict(config)
    m.create()
    assert m.exists()
    assert m.permission["uid"] == 2000
    m.delete()
    assert not m.mountpoint.exists()
    
    