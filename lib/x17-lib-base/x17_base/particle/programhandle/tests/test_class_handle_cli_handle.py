import pytest
import re
from x17_base.particle.terminal.command import Command
from x17_base.particle.terminal.terminal import Terminal
from x17_base.particle.programhandle.cli import CliHandle

def test_cli_is_available():
    handle = CliHandle("git")
    assert handle.is_available

def test_cli_get_version():
    handle = CliHandle("python3")
    version = handle.get_version()
    assert isinstance(version, str)
    assert re.match(r'\d+\.\d+\.\d+', version)

def test_cli_register_and_run():
    handle = CliHandle("python3")
    command = Command("python3 -c 'print(123)'", shell=True)
    handle.register("print_123", command)
    response = handle.run(
        handle.get_registered("print_123"),
    )
    assert response.success
    assert "123" in response.stdout
    
def test_from_name():
    handle = CliHandle.from_name("python3")
    assert isinstance(handle, CliHandle)
    assert handle.name == "python3"


def test_init():
    handle = CliHandle("python3")
    assert handle.name == "python3"
    assert isinstance(handle.terminal, Terminal)
    assert isinstance(handle.registries, dict)


def test_is_available():
    handle = CliHandle("python3")
    assert isinstance(handle.is_available, bool)


def test_dict():
    handle = CliHandle("python3")
    d = handle.dict
    assert "name" in d and "is_available" in d


def test_bool():
    handle = CliHandle("python3")
    assert bool(handle) == handle.is_available


def test_str():
    handle = CliHandle("python3")
    assert str(handle) == "python3"


def test_len():
    handle = CliHandle("python3")
    assert len(handle) in (0, 1)


def test_repr():
    handle = CliHandle("python3")
    assert "CliHandle" in repr(handle)


def test_run():
    handle = CliHandle("python3")
    cmd = Command("python3 -c 'print(123)'", shell=True)
    res = handle.run(cmd)
    assert res.success
    assert "123" in res.stdout


def test_get_version():
    handle = CliHandle("python3")
    version = handle.get_version()
    assert isinstance(version, str)
    assert version.count(".") >= 1


def test_register():
    handle = CliHandle("python3")
    cmd = Command("echo hi", shell=True)
    handle.register("say_hi", cmd)
    assert "say_hi" in handle.registries


def test_register_duplicate_raises():
    handle = CliHandle("python3")
    cmd = Command("echo hi", shell=True)
    handle.register("say_hi", cmd)
    with pytest.raises(ValueError):
        handle.register("say_hi", cmd)


def test_get_registered():
    handle = CliHandle("python3")
    cmd = Command("echo hi", shell=True)
    handle.register("say_hi", cmd)
    assert handle.get_registered("say_hi") == cmd
    assert handle.get_registered("not_exist") is None