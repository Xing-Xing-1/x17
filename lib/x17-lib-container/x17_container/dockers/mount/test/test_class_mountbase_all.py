import pytest
from x17_container.dockers.mount.base import MountBase

@pytest.fixture
def base_mount():
    return MountBase(
        name="base_mount",
        mode="rw",
        chmod=False,
        permission={},
    )

def test_mountbase_defaults(base_mount):
    assert base_mount.name == "base_mount"
    assert base_mount.mode == "rw"
    assert base_mount.chmod is False
    assert base_mount.permission == {}

def test_mountbase_lifecycle_methods(base_mount):
    assert base_mount.exists() is False
    assert base_mount.reload() is None
    assert base_mount.refresh() is None
    assert base_mount.create() is None
    assert base_mount.delete() is None

