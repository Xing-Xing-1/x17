import pytest
import os
import json
from pathlib import Path
from moto.particle.custom.tagset import BaseTagset
from moto.particle.custom.xmeta import XMeta  # Adjust the import path as needed


@pytest.fixture
def test_env_dir():
    """
    Ensure the tests/env/ directory exists and return its Path object.
    """
    base_dir = Path("tests/env")
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


@pytest.fixture
def temp_file(test_env_dir):
    """
    Create a temporary file in tests/env/ for testing.
    """
    file = test_env_dir / "test.txt"
    file.write_text("This is a test file.")
    return file


@pytest.fixture
def temp_dir(test_env_dir):
    """
    Create a temporary directory in tests/env/ for testing.
    """
    dir_path = test_env_dir / "test_dir"
    dir_path.mkdir(exist_ok=True)
    return dir_path


def test_xmeta_init_file(temp_file):
    """
    Test initializing XMeta with a file.
    """
    xmeta = XMeta(item_path=str(temp_file))
    assert xmeta.src_exists is True
    assert xmeta.src_is_file is True
    assert xmeta.src_is_dir is False
    assert xmeta.src_name == temp_file.name
    assert xmeta.src_suffix == temp_file.suffix
    assert xmeta.path.name.endswith(".xmeta")


def test_xmeta_init_dir(temp_dir):
    """
    Test initializing XMeta with a directory.
    """
    xmeta = XMeta(item_path=str(temp_dir))
    assert xmeta.src_exists is True
    assert xmeta.src_is_file is False
    assert xmeta.src_is_dir is True
    assert xmeta.src_name == temp_dir.name
    assert xmeta.src_suffix == ""


def test_xmeta_non_existent_file(test_env_dir):
    """
    Test initializing XMeta with a non-existent file.
    """
    non_existent_file = test_env_dir / "non_existent_file.txt"
    xmeta = XMeta(item_path=str(non_existent_file))
    assert not xmeta.src_exists
    assert not xmeta.src_is_file
    assert not xmeta.src_is_dir
    assert xmeta.path.name == f".{non_existent_file.name}.xmeta"
    assert not xmeta.exists  # Metadata file should not exist


def test_xmeta_non_existent_dir(test_env_dir):
    """
    Test initializing XMeta with a non-existent directory.
    """
    non_existent_dir = test_env_dir / "non_existent_dir"
    xmeta = XMeta(item_path=str(non_existent_dir))
    assert not xmeta.src_exists
    assert not xmeta.src_is_file
    assert not xmeta.src_is_dir
    assert xmeta.path.name == f".{non_existent_dir.name}.xmeta"
    assert not xmeta.exists 


def test_xmeta_write_for_non_existent_file(test_env_dir):
    """
    Test writing metadata for a non-existent file.
    """
    non_existent_file = test_env_dir / "non_existent_file.txt"
    xmeta = XMeta(item_path=str(non_existent_file))
    try:
        xmeta.write()
    except Exception as e:
        assert FileNotFoundError in e.__class__.__mro__

def test_xmeta_delete_for_non_existent_file(test_env_dir):
    """
    Test deleting metadata for a non-existent file.
    """
    non_existent_file = test_env_dir / "non_existent_file.txt"
    xmeta = XMeta(item_path=str(non_existent_file))
    xmeta.delete()
    assert not xmeta.exists  # Metadata file should not exist
