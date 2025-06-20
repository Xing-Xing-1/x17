import os
import shutil
import pytest
from pathlib import Path

from x17_container.dockers.mount.host import MountHost
from x17_container.dockers.mount.volume import MountVolume
from x17_container.dockers.mount.tmpfs import MountTmpfs
from x17_container.dockers.mount.group import MountGroup


@pytest.fixture
def temp_dir(tmp_path):
    yield tmp_path
    if tmp_path.exists():
        shutil.rmtree(tmp_path)


@pytest.fixture
def sample_mounts(temp_dir):
    host = MountHost(
        mountpoint=temp_dir / "host_dir",
        target="/mnt/host_data",
        name="test_host",
        mode="rw",
        chmod=True,
    )
    host2 = MountHost(
        mountpoint=temp_dir / "host_dir2",
        target="/mnt/host_data2",
        name="test_host2",
        mode="ro",
        chmod=False,
    )
    volume = MountVolume(
        name="test_volume",
        mountpoint="/mnt/vol_data",
    )
    volume2 = MountVolume(
        name="test_volume2",
        mountpoint="/mnt/vol_data2",
        mode="rw",
        permission={"uid": 1000, "gid": 1000},
    )
    tmpfs = MountTmpfs(
        target="/mnt/tmpfs_data",
        name="test_tmpfs",
        size=64 * 1024 * 1024,
        mode="rw",
    )
    tmpfs2 = MountTmpfs(
        target="/mnt/tmpfs_data2",
        name="test_tmpfs2",
        size=128 * 1024 * 1024,
        mode="ro",
    )
    return {
        "host": host,
        "host2": host2,
        "volume": volume,
        "volume2": volume2,
        "tmpfs": tmpfs,
        "tmpfs2": tmpfs2,
        "temp_dir": temp_dir,
    }


def test_mountgroup_add_and_query(sample_mounts):
    host = sample_mounts["host"]
    volume = sample_mounts["volume"]
    tmpfs = sample_mounts["tmpfs"]
    temp_dir = sample_mounts["temp_dir"]
    group = MountGroup(name="test_group")
    group.add_mount(host)
    group.add_mount(volume)
    group.add_mount(tmpfs)

    assert group.num_mounts == 3
    assert group.get_mount_by_name("test_host") is host
    assert group.get_mount_by_target("/mnt/host_data") is host
    assert group.get_mount_by_name("test_volume") is volume
    assert group.get_mount_by_mountpoint(temp_dir / "host_dir") is host
    assert group.get_mount_by_mountpoint("/mnt/vol_data") is volume


def test_mountgroup_create_and_exists(sample_mounts):
    host = sample_mounts["host"]
    volume = sample_mounts["volume"]
    tmpfs = sample_mounts["tmpfs"]
    group = MountGroup(
        name="test_group2",
        volumes=[volume],
        hosts=[host],
        tmpfses=[tmpfs],
    )
    group.create()
    assert group.exists()


def test_mountgroup_delete_and_retain(sample_mounts):
    host = sample_mounts["host"]
    volume = sample_mounts["volume"]
    tmpfs = sample_mounts["tmpfs"]
    group = MountGroup(
        name="test_group3",
        volumes=[volume],
        hosts=[host],
        tmpfses=[tmpfs],
        retain_on_delete=False,
    )
    group.create()
    assert group.exists()
    group.delete()
    assert not volume.exists()
    assert not host.exists()


def test_mountgroup_unlink_mount(sample_mounts):
    host = sample_mounts["host"]
    volume = sample_mounts["volume"]
    tmpfs = sample_mounts["tmpfs"]
    group = MountGroup(
        name="test_group4",
        volumes=[volume],
        hosts=[host],
        tmpfses=[tmpfs],
    )
    assert group.unlink_mount(volume) is True
    assert group.num_volumes == 0
    assert group.unlink_mount(volume) is False


def test_mountgroup_docker_conf_keys(sample_mounts):
    host = sample_mounts["host"]
    volume = sample_mounts["volume"]
    tmpfs = sample_mounts["tmpfs"]
    group = MountGroup(
        name="test_group5",
        volumes=[volume],
        hosts=[host],
        tmpfses=[tmpfs],
    )
    conf = group.to_docker_conf()
    assert "tmpfs" in conf
    assert "volumes" in conf


@pytest.mark.integration
def test_mountgroup_integration_lifecycle(sample_mounts):
    host = sample_mounts["host"]
    volume = sample_mounts["volume"]
    tmpfs = sample_mounts["tmpfs"]

    group = MountGroup(
        name="integration_group",
        volumes=[volume],
        hosts=[host],
        tmpfses=[tmpfs],
        retain_on_delete=False,
    )
    group.create()
    assert host.mountpoint.exists()
    assert volume.exists()
    assert group.exists()

    docker_conf = group.to_docker_conf()
    assert "tmpfs" in docker_conf
    assert "volumes" in docker_conf
    assert isinstance(docker_conf["tmpfs"], dict)
    assert isinstance(docker_conf["volumes"], dict)

    group.delete()
    assert not host.exists()
    assert not volume.exists()


@pytest.mark.integration
def test_mountgroup_retain_on_delete_true(sample_mounts):
    volume = sample_mounts["volume"]
    host = sample_mounts["host"]
    group = MountGroup(
        name="retain_group",
        volumes=[volume],
        hosts=[host],
        retain_on_delete=True,
    )
    group.create()
    assert group.exists()
    group.delete()
    assert host.mountpoint.exists()
    assert volume.exists()
    host.delete()
    volume.delete()

@pytest.mark.integration
def test_mountgroup_reload_and_refresh(sample_mounts):
    host = sample_mounts["host"]
    volume = sample_mounts["volume"]
    tmpfs = sample_mounts["tmpfs"]
    group = MountGroup(
        name="reload_refresh_group",
        volumes=[volume],
        hosts=[host],
        tmpfses=[tmpfs],
        retain_on_delete=False,
    )
    group.create()
    group.reload()
    group.refresh()
    assert group.exists()
    group.delete()


@pytest.mark.integration
def test_mountgroup_dict_export(sample_mounts):
    host = sample_mounts["host"]
    volume = sample_mounts["volume"]
    tmpfs = sample_mounts["tmpfs"]
    group = MountGroup(
        name="dict_group",
        volumes=[volume],
        hosts=[host],
        tmpfses=[tmpfs],
        retain_on_delete=False,
    )
    d = group.dict
    assert d["name"] == "dict_group"
    assert d["num_mounts"] == 3
    assert d["num_volumes"] == 1
    assert d["num_hosts"] == 1
    assert d["num_tmpfses"] == 1
    assert d["retain_on_delete"] is False
    
def test_mountgroup_delete_mount(sample_mounts):
    volume = sample_mounts["volume"]
    group = MountGroup(volumes=[volume])
    group.create()
    assert group.delete_mount(volume) is True
    assert group.num_volumes == 0
    

def test_mountgroup_unlink_only_one(sample_mounts):
    host = sample_mounts["host"]
    group = MountGroup(name="unlink_test_group", hosts=[host])
    assert group.num_hosts == 1
    assert group.unlink_mount(host) is True
    assert group.num_hosts == 0
    assert group.unlink_mount(host) is False

def test_mountgroup_multi_mount_types(sample_mounts):
    host = sample_mounts["host"]
    host2 = sample_mounts["host2"]
    volume = sample_mounts["volume"]
    volume2 = sample_mounts["volume2"]
    tmpfs = sample_mounts["tmpfs"]
    tmpfs2 = sample_mounts["tmpfs2"]

    group = MountGroup(
        name="multi_mount_group",
        volumes=[volume, volume2],
        hosts=[host, host2],
        tmpfses=[tmpfs, tmpfs2],
        retain_on_delete=False,
    )
    group.create()
    assert group.num_mounts == 6
    assert group.num_volumes == 2
    assert group.num_hosts == 2
    assert group.num_tmpfses == 2
    assert group.exists()
    group.delete()
    assert not host.exists()
    assert not volume.exists()
    
