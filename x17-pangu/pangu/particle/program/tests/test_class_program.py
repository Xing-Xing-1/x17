import pytest
from unittest.mock import MagicMock
from pangu.particle.program import Program

def mock_handle(name, available=True):
    handle = MagicMock()
    handle.name = name
    handle.is_available = available
    handle.dict = {"name": name, "is_available": available}
    return handle

def test_program_with_no_handles():
    prog = Program(name="empty")
    assert prog.is_available is False
    assert bool(prog) is False
    assert isinstance(prog.dict, dict)
    assert all(v is None for v in prog.dict["handles"].values())

def test_program_with_some_handles():
    cli = mock_handle("cli", True)
    web = mock_handle("web", False)
    prog = Program(name="some", cli=cli, web=web)
    assert prog.is_available is True
    assert bool(prog) is True
    d = prog.dict
    assert d["handles"]["cli"]["is_available"] is True
    assert d["handles"]["web"]["is_available"] is False
    assert d["handles"]["daemon"] is None

def test_program_with_all_unavailable_handles():
    handles = {name: mock_handle(name, False) for name in ["cli", "daemon", "web", "gui", "service"]}
    prog = Program(name="none", **handles)
    assert prog.is_available is False
    assert bool(prog) is False
    for v in prog.dict["handles"].values():
        assert v["is_available"] is False

def test_program_with_all_available_handles():
    handles = {name: mock_handle(name, True) for name in ["cli", "daemon", "web", "gui", "service"]}
    prog = Program(name="all", **handles)
    assert prog.is_available is True
    assert bool(prog) is True
    for v in prog.dict["handles"].values():
        assert v["is_available"] is True