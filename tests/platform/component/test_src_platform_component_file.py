#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.platform.macos.component.file import File  # type: ignore
from moto.particle.storage import storage  # type: ignore

import pytest  # type: ignore
import os  # type: ignore

cwd = os.getcwd()


@pytest.fixture
def remote_file_instance():
    file = File()
    return file


@pytest.fixture
def sample_file_instance():
    test_env_path = "tests/env/"
    test_env_key = f"{test_env_path}sample.txt"
    file = File(test_env_key)
    return file


def test_remote_file_init(remote_file_instance):
    assert remote_file_instance.path == None
    assert remote_file_instance.full_path == None
    assert remote_file_instance.name == None
    assert remote_file_instance.suffix == None
    assert remote_file_instance.exists == False
    assert remote_file_instance.id == None
    assert remote_file_instance.create_at == None
    assert remote_file_instance.modify_at == None
    assert remote_file_instance.access_at == None
    assert remote_file_instance.size == storage(0)
    assert remote_file_instance.is_file == None
    assert remote_file_instance.is_dir == None
    assert remote_file_instance.is_hidden == None
    assert remote_file_instance.content == None


def test_sample_file_init(sample_file_instance):
    assert sample_file_instance.path.as_posix() == f"tests/env/sample.txt"
    assert sample_file_instance.full_path.as_posix() == f"{cwd}/tests/env/sample.txt"
    assert sample_file_instance.name == "sample.txt"
    assert sample_file_instance.suffix == ".txt"
    assert sample_file_instance.exists == True
    assert sample_file_instance.id != None
    assert sample_file_instance.create_at != None
    assert sample_file_instance.modify_at != None
    assert sample_file_instance.access_at != None
    assert sample_file_instance.size != storage(0)
    assert sample_file_instance.is_file == True
    assert sample_file_instance.is_dir == False
    assert sample_file_instance.is_hidden == False
    assert sample_file_instance.content == None


def test_remote_file_str(remote_file_instance):
    assert str(remote_file_instance) == "None"


def test_sample_file_str(sample_file_instance):
    assert str(sample_file_instance) == "sample.txt"


def test_remote_file_dict(remote_file_instance):
    assert remote_file_instance.__dict__() == {
        "path": None,
        "full_path": None,
        "name": None,
        "suffix": None,
        "exists": False,
        "id": None,
        "create_at": None,
        "modify_at": None,
        "access_at": None,
        "size": str(storage(0)),
        "is_file": None,
        "is_dir": None,
        "is_hidden": None,
    }


def test_sample_file_dict(sample_file_instance):
    assert sample_file_instance.__dict__() == {
        "path": f"tests/env/sample.txt",
        "full_path": f"{cwd}/tests/env/sample.txt",
        "name": "sample.txt",
        "suffix": ".txt",
        "exists": True,
        "id": str(sample_file_instance.id),
        "create_at": str(sample_file_instance.create_at),
        "modify_at": str(sample_file_instance.modify_at),
        "access_at": str(sample_file_instance.access_at),
        "size": str(sample_file_instance.size),
        "is_file": True,
        "is_dir": False,
        "is_hidden": False,
    }


def test_remote_file_set(remote_file_instance):
    remote_file_instance.set(b"")
    assert remote_file_instance.content == b""


def test_sample_file_set_bytes(sample_file_instance):
    sample_file_instance.set(b"hello world")
    assert sample_file_instance.content == b"hello world"


def test_remote_file_write(remote_file_instance):
    try:
        remote_file_instance.write("hello world")
    except Exception as e:
        assert "expected str, bytes or os.PathLike object, not NoneType" in str(e)


def test_sample_file_write(sample_file_instance):
    sample_file_instance.write("hello world")
    sample_file_reload = File(f"{cwd}/tests/env/sample.txt")
    assert sample_file_reload.read() == "hello world"

    sample_file_instance.write("hello world", mode="w+")
    sample_file_reload = File(f"{cwd}/tests/env/sample.txt")
    assert sample_file_reload.read() == "hello world"


def test_remote_file_write_bytes(remote_file_instance):
    try:
        remote_file_instance.write_bytes(b"hello world")
    except Exception as e:
        assert "expected str, bytes or os.PathLike object, not NoneType" in str(e)


def test_sample_file_write_bytes(sample_file_instance):
    sample_file_instance.write_bytes(b"hello world")
    sample_file_reload = File(f"{cwd}/tests/env/sample.txt")
    assert sample_file_reload.read_bytes() == b"hello world"


def test_remote_file_append_write(remote_file_instance):
    try:
        remote_file_instance.write("hello world", mode="a")
    except Exception as e:
        assert "expected str, bytes or os.PathLike object, not NoneType" in str(e)


def test_sample_file_append_write(sample_file_instance):
    sample_file_instance.write("!", mode="a")
    sample_file_reload = File(f"{cwd}/tests/env/sample.txt")
    assert sample_file_reload.read() == "hello world!"

    sample_file_instance.write("hello world", mode="w+")
    sample_file_reload = File(f"{cwd}/tests/env/sample.txt")
    assert sample_file_reload.read() == "hello world"


def test_remote_file_read(remote_file_instance):
    assert remote_file_instance.read() == None


def test_sample_file_read(sample_file_instance):
    assert sample_file_instance.read(mode="rb") == b"hello world"


def test_remote_file_read_bytes(remote_file_instance):
    assert remote_file_instance.read_bytes() == None


def test_sample_file_read_bytes(sample_file_instance):
    assert sample_file_instance.read_bytes() == b"hello world"


def test_remote_file_read_text(remote_file_instance):
    assert remote_file_instance.read_text() == None


def test_sample_file_read_text(sample_file_instance):
    assert sample_file_instance.read_text() == "hello world"


def test_sample_file_copy(sample_file_instance):
    copy_file_instance = sample_file_instance.copy("tests/env/sample_copy.txt")
    assert copy_file_instance.exists == True
    assert copy_file_instance.read() == "hello world"
    copy_file_instance.delete()


def test_sample_file_copy_force(sample_file_instance):
    copy_file_instance = sample_file_instance.copy("tests/env/sample_copy.txt")
    assert copy_file_instance.exists == True
    assert copy_file_instance.read() == "hello world"
    copy_file_instance = sample_file_instance.copy(
        "tests/env/sample_copy.txt", force=True
    )
    assert copy_file_instance.exists == True
    assert copy_file_instance.read() == "hello world"
    copy_file_instance.delete()


def test_sample_file_copydir(sample_file_instance):
    copy_file_instance = sample_file_instance.copy("tests/env/sample_copy/")
    assert copy_file_instance.exists == True
    assert copy_file_instance.read() == "hello world"
    copy_file_instance.delete()


def test_sample_file_move(sample_file_instance):
    move_file_instance = sample_file_instance.copy(
        "tests/env/sample_move.txt", force=True
    )
    assert move_file_instance.exists == True
    assert move_file_instance.read() == "hello world"
    move_file_instance.move("tests/env/sample_moved.txt")
    assert move_file_instance.exists == True
    assert move_file_instance.read() == "hello world"
    move_file_instance.delete()


def test_sample_file_delete(sample_file_instance):
    delete_file_instance = sample_file_instance.copy(
        "tests/env/sample_delete.txt", force=True
    )
    assert delete_file_instance.exists == True
    assert delete_file_instance.read() == "hello world"
    delete_file_instance.delete()
    assert delete_file_instance.exists == False


def test_sample_file_rename(sample_file_instance):
    rename_file_instance = sample_file_instance.copy(
        "tests/env/sample_rename.txt", force=True
    )
    assert rename_file_instance.exists == True
    assert rename_file_instance.read() == "hello world"
    rename_file_instance.rename("sample_renamed.txt")
    assert rename_file_instance.exists == True
    assert rename_file_instance.read() == "hello world"
    rename_file_instance.delete()
