import pytest
from pangu.particle.terminal.terminal import Terminal
from pangu.particle.program.handle.cli import CLIHandle

@pytest.fixture
def handle():
    terminal = Terminal()
    return CLIHandle(name="echo", terminal=terminal)

def test_is_available(handle):
    assert handle.is_available() is True

def test_run_string_args(handle):
    response = handle.run("hello pytest")
    assert response.code == 0
    assert "hello pytest" in response.stdout

def test_run_list_args(handle):
    response = handle.run(["hello", "list"])
    assert response.code == 0
    assert "hello list" in response.stdout

def test_get_version_on_echo(handle):
    version = handle.get_version(option="--version")  # echo may not support this
    assert isinstance(version, str)  # should still return a string (possibly empty)

def test_handle_with_invalid_command():
    terminal = Terminal()
    bad_handle = CLIHandle(name="nonexistent_1234567", terminal=terminal)
    assert not bad_handle.is_available()