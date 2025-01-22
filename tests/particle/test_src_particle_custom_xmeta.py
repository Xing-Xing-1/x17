from pathlib import Path
import pytest # type: ignore
import os

from moto.particle.custom.tagset import BaseTagset
from moto.particle.custom.xmeta import XMeta  # Adjust the import path as needed

cwd = os.getcwd()

@pytest.fixture
def temp_file():
    return XMeta(
        item_path = f"{cwd}/tests/env/test.txt"
    )


@pytest.fixture
def temp_dir():
    return XMeta(
        item_path = f"{cwd}/tests/env/"
    )


def test_xmeta_init_file(temp_file):
    """
    Test initializing XMeta with a file.
    """
    assert temp_file.src_exists is True
    assert temp_file.src_is_file is True
    assert temp_file.src_is_dir is False
    assert temp_file.src_name == "test.txt"
    assert temp_file.src_suffix == ".txt"
    assert temp_file.src_path.name.endswith("txt")


def test_xmeta_init_dir(temp_dir):
    """
    Test initializing XMeta with a directory.
    """
    assert temp_dir.src_exists is True
    assert temp_dir.src_is_file is False
    assert temp_dir.src_is_dir is True
    assert temp_dir.src_name == "env"
    assert temp_dir.src_suffix == ""
    assert temp_dir.src_path.name.endswith("")


def test_xmeta_init_non_existent_file():
    """
    Test initializing XMeta with a non-existent file.
    """
    non_existent_file = f"{cwd}tests/env/non_existent_file.txt"
    xmeta = XMeta(item_path=str(non_existent_file))
    assert not xmeta.src_exists
    assert not xmeta.src_is_file
    assert not xmeta.src_is_dir
    assert xmeta.path.name == f".non_existent_file.txt.xmeta"
    assert not xmeta.exists  # Metadata file should not exist


def test_xmeta_init_non_existent_dir():
    """
    Test initializing XMeta with a non-existent directory.
    """
    non_existent_dir = f"{cwd}tests/env/non_existent_dir"
    xmeta = XMeta(item_path=str(non_existent_dir))
    assert not xmeta.src_exists
    assert not xmeta.src_is_file
    assert not xmeta.src_is_dir
    assert xmeta.path.name == f".non_existent_dir.xmeta"
    assert not xmeta.exists 

