from moto.particle.base.item import BaseItem # type: ignore
from moto.particle.storage import storage  # type: ignore

import pytest  # type: ignore
import os  # type: ignore

cwd = os.getcwd()

@pytest.fixture
def remote_item_instance():
    return BaseItem()

@pytest.fixture
def sample_item_file():
    test_env_path = "tests/env/sample.txt"
    return BaseItem(test_env_path)

@pytest.fixture
def sample_item_folder():
    test_env_path = "tests/env/sample_folder/"
    return BaseItem(test_env_path)



def test_set(remote_item_instance, sample_item_file, sample_item_folder):
    remote_item_instance.set(None)
    assert remote_item_instance.path is None
    assert remote_item_instance.full_path is None
    assert remote_item_instance.name is None
    assert remote_item_instance.exists is False
    assert remote_item_instance.id is None
    assert remote_item_instance.create_at is None
    assert remote_item_instance.modify_at is None
    assert remote_item_instance.access_at is None
    assert remote_item_instance.size == storage(0)
    assert remote_item_instance.is_file is None
    assert remote_item_instance.is_dir is None
    assert remote_item_instance.is_hidden is None

    test_env_path = "tests/env/sample.txt"
    sample_item_file.set(test_env_path)
    assert sample_item_file.path is not None
    assert sample_item_file.full_path is not None
    assert sample_item_file.name is not None
    assert sample_item_file.exists is True
    assert sample_item_file.id is not None
    assert sample_item_file.create_at is not None
    assert sample_item_file.modify_at is not None
    assert sample_item_file.access_at is not None
    assert sample_item_file.size is not storage(0)
    assert sample_item_file.is_file == True
    assert sample_item_file.is_dir == False
    assert sample_item_file.is_hidden is not None

    test_env_path = "tests/env/sample_folder/"
    sample_item_folder.set(test_env_path)
    assert sample_item_folder.path is not None
    assert sample_item_folder.full_path is not None
    assert sample_item_folder.name is not None
    assert sample_item_folder.exists is True
    assert sample_item_folder.id is not None
    assert sample_item_folder.create_at is not None
    assert sample_item_folder.modify_at is not None
    assert sample_item_folder.access_at is not None
    assert sample_item_folder.size is not storage(0)
    assert sample_item_folder.is_file == False
    assert sample_item_folder.is_dir == True
    assert sample_item_folder.is_hidden is not None


def test_get_str(remote_item_instance, sample_item_file, sample_item_folder):
    assert str(remote_item_instance) == f"BaseItem(name={remote_item_instance.name}, path={remote_item_instance.get_path(as_str=True)})"
    assert str(sample_item_file) == f"BaseItem(name={sample_item_file.name}, path={sample_item_file.get_path(as_str=True)})"
    assert str(sample_item_folder) == f"BaseItem(name={sample_item_folder.name}, path={sample_item_folder.get_path(as_str=True)})"

def test_get_dict(remote_item_instance, sample_item_file, sample_item_folder):
    assert remote_item_instance.__dict__() == {
        "path": None,
        "full_path": None,
        "name": None,
        "exists": False,
        "id": None,
        "create_at": None,
        "modify_at": None,
        "access_at": None,
        "size": 0,
        "is_file": None,
        "is_dir": None,
        "is_hidden": None,
    }
    remote_item_dict = remote_item_instance.__dict__()
    assert remote_item_dict["path"] == None
    remote_item_dict["full_path"] == None
    remote_item_dict["name"] == None
    remote_item_dict["exists"] == False
    remote_item_dict["id"] == None
    remote_item_dict["create_at"] == None
    remote_item_dict["modify_at"] == None
    remote_item_dict["access_at"] == None
    remote_item_dict["size"] == 0
    remote_item_dict["is_file"] == None
    remote_item_dict["is_dir"] == None
    remote_item_dict["is_hidden"] == None

    sample_item_file_dict = sample_item_file.__dict__()
    assert sample_item_file_dict["path"] == "tests/env/sample.txt"
    sample_item_file_dict["full_path"] == f"{cwd}/tests/env/sample.txt"
    sample_item_file_dict["name"] == "sample.txt"
    sample_item_file_dict["exists"] == True
    sample_item_file_dict["id"] is not None
    sample_item_file_dict["create_at"] is not None
    sample_item_file_dict["modify_at"] is not None
    sample_item_file_dict["access_at"] is not None
    sample_item_file_dict["size"] is not storage(0)
    sample_item_file_dict["is_file"] == True
    sample_item_file_dict["is_dir"] == False
    sample_item_file_dict["is_hidden"] is not None
    
    sample_item_folder_dict = sample_item_folder.__dict__()
    assert sample_item_folder_dict["path"] == "tests/env/sample_folder"
    sample_item_folder_dict["full_path"] == f"{cwd}/tests/env/sample_folder"
    sample_item_folder_dict["name"] == "sample_folder"
    sample_item_folder_dict["exists"] == True
    sample_item_folder_dict["id"] is not None
    sample_item_folder_dict["create_at"] is not None
    sample_item_folder_dict["modify_at"] is not None
    sample_item_folder_dict["access_at"] is not None
    sample_item_folder_dict["size"] is not storage(0)
    sample_item_folder_dict["is_file"] == False
    sample_item_folder_dict["is_dir"] == True
    sample_item_folder_dict["is_hidden"] is not None


def test_set(remote_item_instance, sample_item_file, sample_item_folder):
    test_env_path = "tests/env/sample_folder/"
    remote_item_instance.set(test_env_path)
    assert remote_item_instance.path is not None
    assert remote_item_instance.full_path is not None
    assert remote_item_instance.name is not None
    assert remote_item_instance.exists is True

    test_env_path = "tests/env/sample.txt"
    sample_item_file.set(test_env_path)
    assert sample_item_file.path is not None
    assert sample_item_file.full_path is not None
    assert sample_item_file.name is not None
    assert sample_item_file.exists is True

    test_env_path = "tests/env/sample_folder/"
    sample_item_folder.set(test_env_path)
    assert sample_item_folder.path is not None
    assert sample_item_folder.full_path is not None
    assert sample_item_folder.name is not None
    assert sample_item_folder.exists is True

def test_get_name(remote_item_instance, sample_item_file, sample_item_folder):
    assert remote_item_instance.get_name() == None
    assert sample_item_file.get_name() == "sample.txt"
    assert sample_item_folder.get_name() == "sample_folder"

def test_get_path(remote_item_instance, sample_item_file, sample_item_folder):
    assert remote_item_instance.get_path(as_str=True) == None
    assert sample_item_file.get_path(as_str=True) == "tests/env/sample.txt"
    assert sample_item_folder.get_path(as_str=True) == "tests/env/sample_folder"

def test_get_fullpath(remote_item_instance, sample_item_file, sample_item_folder):
    assert remote_item_instance.get_fullpath(as_str=True) == None
    assert sample_item_file.get_fullpath(as_str=True) == f"{cwd}/tests/env/sample.txt"
    assert sample_item_folder.get_fullpath(as_str=True) == f"{cwd}/tests/env/sample_folder"

def test_check_exists(remote_item_instance, sample_item_file, sample_item_folder):
    assert remote_item_instance.check_exists() == False
    assert sample_item_file.check_exists() == True
    assert sample_item_folder.check_exists() == True

def test_eq(remote_item_instance, sample_item_file, sample_item_folder):
    assert remote_item_instance == remote_item_instance
    assert sample_item_file == sample_item_file
    assert sample_item_folder == sample_item_folder
    assert remote_item_instance != sample_item_file
    assert remote_item_instance != sample_item_folder
    assert sample_item_file != sample_item_folder
    assert sample_item_file != remote_item_instance
    assert sample_item_folder != remote_item_instance
    assert sample_item_folder != sample_item_file

def test_get_permission(remote_item_instance, sample_item_file, sample_item_folder):
    assert remote_item_instance.get_permission() == None
    assert sample_item_file.get_permission() != None
    assert sample_item_folder.get_permission() != None