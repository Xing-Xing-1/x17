import pytest
from unittest.mock import MagicMock
from x17_base.particle.terminal.command import Command
from x17_base.particle.programhandle.service import ServiceHandle
from x17_base.particle.terminal.terminal import Terminal

def test_is_available_true(monkeypatch):
    terminal = Terminal()
    monkeypatch.setattr(terminal, "find_process", lambda keyword, **kwargs: ["proc1"])
    handle = ServiceHandle(name="demo", terminal=terminal)
    assert handle.is_available is True
    assert bool(handle) is True
    assert len(handle) == 1

def test_is_available_false(monkeypatch):
    terminal = Terminal()
    monkeypatch.setattr(terminal, "find_process", lambda keyword, **kwargs: [])
    handle = ServiceHandle(name="demo", terminal=terminal)
    assert handle.is_available is False
    assert bool(handle) is False
    assert len(handle) == 0

def test_register_and_get_registered():
    handle = ServiceHandle(name="demo")
    cmd = Command("echo hello")
    handle.register("say_hello", cmd)
    assert handle.get_registered("say_hello") == cmd

def test_register_as_method(monkeypatch):
    terminal = Terminal()
    monkeypatch.setattr(terminal, "find_process", lambda keyword, **kwargs: [])
    handle = ServiceHandle(name="demo", terminal=terminal)
    mock_cmd = Command("echo world")
    handle.terminal.run = MagicMock(return_value="ok")
    handle.register("test_run", mock_cmd, as_method=True)
    assert hasattr(handle, "test_run")
    result = handle.test_run()
    assert result == "ok"