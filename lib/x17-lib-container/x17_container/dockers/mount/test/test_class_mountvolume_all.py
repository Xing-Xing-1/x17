import pytest
import docker
from docker.errors import NotFound
from x17_container.dockers.mount.volume import MountVolume

@pytest.fixture(scope="module")
def docker_client():
    return docker.from_env()

@pytest.fixture
def temp_volume(docker_client):
    name = "test_mount_volume"
    try:
        vol = docker_client.volumes.get(name)
        vol.remove(force=True)
    except NotFound:
        pass
    volume = docker_client.volumes.create(name=name)
    yield volume
    volume.remove(force=True)

@pytest.fixture
def mount_volume(temp_volume, docker_client):
    return MountVolume.from_docker(
        docker_volume=temp_volume,
        docker_client=docker_client,
        chmod=True,
        permission={"uid": 1000, "gid": 1000, "mode": 0o777},
        mode="rw",
    )

def test_mountvolume_load(mount_volume):
    assert mount_volume.name == "test_mount_volume"
    assert mount_volume.mountpoint is not None
    assert mount_volume.driver == "local"

def test_mountvolume_dict(mount_volume):
    data = mount_volume.dict
    assert data["name"] == "test_mount_volume"
    assert "mountpoint" in data
    assert data["chmod"] is True
    assert data["permission"]["uid"] == 1000

def test_mountvolume_permission_script(mount_volume):
    script = mount_volume.permission_script
    assert "chown -R 1000:1000" in script
    assert "chmod -R 777" in script

def test_mountvolume_chmod_script(mount_volume):
    assert mount_volume.chmod_script is None
    # since permission_script already handles chmod

def test_mountvolume_eq(mount_volume, docker_client):
    other = MountVolume.from_docker(
        docker_volume=docker_client.volumes.get("test_mount_volume"),
        docker_client=docker_client,
    )
    assert mount_volume == other
    assert not (mount_volume != other)

def test_mountvolume_to_docker_volume(mount_volume):
    docker_vol = mount_volume.to_docker_volume()
    assert "test_mount_volume" in docker_vol
    assert docker_vol["test_mount_volume"]["mode"] == "rw"

def test_mountvolume_exists(mount_volume):
    assert mount_volume.exists() is True

def test_mountvolume_reload(mount_volume):
    mount_volume.reload()
    assert mount_volume.driver == "local"
    

@pytest.fixture
def integrate_volume(docker_client):
    name = "test_integrate_volume"
    try:
        docker_client.volumes.get(name).remove(force=True)
    except docker.errors.NotFound:
        pass

    mv = MountVolume(
        name=name,
        chmod=True,
        docker_client=docker_client,
        permission={"uid": 1000, "gid": 1000, "mode": 0o777},
    )
    mv.create()
    yield mv
    mv.delete()

def test_mountvolume_creation(integrate_volume):
    assert integrate_volume.exists()
    assert integrate_volume.name == "test_integrate_volume"
    assert integrate_volume.mountpoint is not None

def test_mountvolume_dict(integrate_volume):
    d = integrate_volume.dict
    assert isinstance(d, dict)
    assert d["name"] == "test_integrate_volume"
    assert "mountpoint" in d

def test_mountvolume_str_repr(integrate_volume):
    assert str(integrate_volume) == "test_integrate_volume"
    assert "test_integrate_volume" in repr(integrate_volume)

def test_mountvolume_eq_ne(docker_client):
    mv1 = MountVolume(name="volume_eq_test", docker_client=docker_client)
    mv2 = MountVolume(name="volume_eq_test", docker_client=docker_client)
    mv3 = MountVolume(name="volume_diff", docker_client=docker_client)
    assert mv1 == mv2
    assert mv1 != mv3

def test_mountvolume_permission_script(integrate_volume):
    script = integrate_volume.permission_script
    assert "chown" in script
    assert "chmod" in script

def test_mountvolume_to_docker_volume(integrate_volume):
    docker_def = integrate_volume.to_docker_volume()
    assert isinstance(docker_def, dict)
    assert integrate_volume.name in docker_def

def test_mountvolume_reload(integrate_volume):
    integrate_volume.reload()
    assert integrate_volume.mountpoint is not None

def test_mountvolume_delete_and_recreate(docker_client):
    name = "volume_recreate_test"
    mv = MountVolume(name=name, docker_client=docker_client)
    mv.create()
    assert mv.exists()
    mv.delete()
    assert not mv.exists()
    mv.create()
    assert mv.exists()
    mv.delete()
    
    