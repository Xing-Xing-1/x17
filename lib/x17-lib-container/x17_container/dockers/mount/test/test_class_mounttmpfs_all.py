import docker
import pytest
from pathlib import Path
from x17_container.dockers.mount.tmpfs import MountTmpfs
from x17_base.particle.storage.storage import Storage

@pytest.fixture(scope="module")
def docker_client():
    return docker.from_env()

@pytest.fixture
def mount_tmpfs():
    return MountTmpfs(
        target="/app/tmpfs",
        name="x17_test_tmpfs_mount",
        size=128,
        mode="rw",
        chmod=False,
        permission={"uid": 1000, "gid": 1000},
        verbose=True,
    )

def test_tmpfs_key_generation(mount_tmpfs):
    assert isinstance(mount_tmpfs.key, str)
    assert len(mount_tmpfs.key) == 64

def test_tmpfs_octal_mode_mapping(mount_tmpfs):
    assert mount_tmpfs.octal_mode == "0755"

def test_tmpfs_dict_content(mount_tmpfs):
    data = mount_tmpfs.dict
    assert data["mode"] == "rw"
    assert data["octal_mode"] == "0755"
    assert data["size"] == 128
    assert data["permission"]["uid"] == 1000

def test_tmpfs_to_docker_tmpfs_format(mount_tmpfs):
    docker_tmpfs = mount_tmpfs.to_docker_tmpfs()
    assert isinstance(docker_tmpfs, dict)
    assert "/app/tmpfs" in docker_tmpfs
    opts = docker_tmpfs["/app/tmpfs"].split(",")
    assert "size=128m" in opts
    assert "uid=1000" in opts
    assert "gid=1000" in opts
    assert "mode=0755" in opts

def test_tmpfs_str_repr_eq(mount_tmpfs):
    other = MountTmpfs(
        target=mount_tmpfs.target,
        size=mount_tmpfs.size,
        mode=mount_tmpfs.mode,
        name=mount_tmpfs.name,
    )
    assert str(mount_tmpfs) == mount_tmpfs.name
    assert repr(mount_tmpfs).startswith("MountTmpfs(")
    assert mount_tmpfs == other
    assert not (mount_tmpfs != other)
    
    
def test_key_is_deterministic(mount_tmpfs):
    key1 = mount_tmpfs.key
    key2 = MountTmpfs(target="/tmp/test-tmpfs", name="tmpfs-test").key
    assert key1 != key2
    key3 = MountTmpfs(target="/tmp/test-tmpfs", name="tmpfs-test").key
    assert key2 == key3

def test_repr_and_str(mount_tmpfs):
    assert repr(mount_tmpfs).startswith("MountTmpfs(")
    assert str(mount_tmpfs) == "x17_test_tmpfs_mount"

def test_eq_and_ne():
    m1 = MountTmpfs(target="/x", name="a", size=64, mode="rw")
    m2 = MountTmpfs(target="/x", name="a", size=64, mode="rw")
    m3 = MountTmpfs(target="/y", name="a", size=64, mode="rw")
    assert m1 == m2
    assert m1 != m3

def test_default_storage_conversion():
    m = MountTmpfs(target="/tmp/test", name="convert-test", size=Storage(256, "mb"))
    assert isinstance(m.size, int)
    assert m.size == 256 * 1024 * 1024  # Convert MB to bytes

def test_dict_output(mount_tmpfs):
    d = mount_tmpfs.dict
    assert isinstance(d, dict)
    assert d["name"] == "x17_test_tmpfs_mount"
    assert d["size"] == 128
    assert d["mode"] == "rw"
    assert d["octal_mode"] == "0755"

def test_to_docker_tmpfs_with_all_options(mount_tmpfs):
    output = mount_tmpfs.to_docker_tmpfs()
    assert "{}".format(mount_tmpfs.target) in output
    assert "size=128m" in output["{}".format(mount_tmpfs.target)]
    assert "uid=1000" in output["{}".format(mount_tmpfs.target)]
    assert "gid=1000" in output["{}".format(mount_tmpfs.target)]
    assert "mode=0755" in output["{}".format(mount_tmpfs.target)]

def test_null_returns():
    m = MountTmpfs(target="/tmp/null", name="null-test")
    assert m.chmod_script is None
    assert m.permission_script is None
    assert m.to_docker_host() is None
    assert m.to_docker_volume() is None
    assert m.get_docker_volume() is None
    

@pytest.fixture(scope="function")
def cleanup_container():
    container_list = []

    def _register(container):
        container_list.append(container)
        return container

    yield _register

    for c in container_list:
        try:
            c.remove(force=True)
        except Exception:
            pass
