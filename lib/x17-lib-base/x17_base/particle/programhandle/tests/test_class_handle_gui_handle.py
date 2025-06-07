import pytest
from unittest.mock import MagicMock
from x17_base.particle.programhandle.gui import GuiHandle
from x17_base.particle.terminal.command import Command

@pytest.fixture
def mocked_gui():
    terminal = MagicMock()
    terminal.exist.return_value = True
    return GuiHandle(name="MockApp", path="/mock/path/MockApp.app", terminal=terminal)

def test_is_available_true(mocked_gui):
    assert mocked_gui.is_available is True
    assert bool(mocked_gui)
    assert len(mocked_gui) == 1

def test_dict_output(mocked_gui):
    d = mocked_gui.dict
    assert d["name"] == "MockApp"
    assert d["is_available"] is True

def test_str_and_repr(mocked_gui):
    assert str(mocked_gui) == "MockApp"
    assert "GuiHandle(" in repr(mocked_gui)

def test_get_version_default(mocked_gui):
    assert mocked_gui.get_version() == "Not Supported"

def test_register_and_get_registered(mocked_gui):
    command = Command(cmd="echo Hello", shell=True)
    mocked_gui.register("hello", command)
    assert mocked_gui.get_registered("hello") == command

def test_register_as_method(mocked_gui):
    command = Command(cmd="echo Hi", shell=True)
    mocked_gui.terminal.run.return_value.success = True
    mocked_gui.register("hi", command, as_method=True)
    assert hasattr(mocked_gui, "hi")
    result = mocked_gui.hi()
    assert result.success