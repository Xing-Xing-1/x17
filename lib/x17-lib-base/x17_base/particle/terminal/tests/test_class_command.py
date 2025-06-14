import os

import pytest
from x17_base.particle.duration import Duration
from x17_base.particle.terminal.command import Command


def test_command_init_default():
    cmd = Command(cmd="echo hello")
    assert cmd.cmd == "echo hello"
    assert cmd.cwd == os.getcwd()
    assert isinstance(cmd.shell, bool) or cmd.shell is None
    assert isinstance(cmd.timeout, Duration)
    assert cmd.encoding == "utf-8"
    assert cmd.text is True
    assert cmd.output is True


def test_command_list_parsing():
    cmd = Command(cmd='git commit -m "message content"')
    assert cmd.list == ["git", "commit", "-m", "message content"]


def test_command_str_output():
    cmd = Command(cmd="ls -la /tmp")
    assert str(cmd) == "ls -la /tmp"


def test_command_repr_output():
    cmd = Command(cmd="python script.py")
    output = repr(cmd)
    assert output.startswith("Command(")
    assert "cmd=python script.py" in output
    assert "cwd=" in output


def test_command_dict_and_export():
    cmd = Command(
        cmd="make build", cwd="/tmp", encoding="utf-8", text=True, output=False
    )
    d = cmd.dict
    assert d["cmd"] == "make build"
    assert d["cwd"] == "/tmp"
    assert d["env"] == {}
    assert isinstance(d["shell"], bool) or d["shell"] is None
    assert isinstance(d["timeout"], dict)
    assert d["encoding"] == "utf-8"
    assert d["text"] is True
    assert d["output"] is False

    exported = cmd.export()
    assert exported == d


def test_command_from_dict():
    d = {
        "cmd": "python app.py",
        "cwd": "/home/user",
        "env": {"DEBUG": "1"},
        "shell": True,
        "timeout": {"second": 30},
        "encoding": "utf-8",
        "text": True,
        "output": True,
    }
    cmd = Command.from_dict(d)
    assert cmd.cmd == "python app.py"
    assert cmd.cwd == "/home/user"
    assert cmd.env == {"DEBUG": "1"}
    assert cmd.shell is True
    assert isinstance(cmd.timeout, Duration)
    assert cmd.timeout.second == 30
    assert cmd.encoding == "utf-8"
    assert cmd.text is True
    assert cmd.output is True


def test_command_add_option_flag_only():
    cmd = Command(cmd="git status")
    cmd.add_option("--short")
    assert "--short" in cmd.list


def test_command_add_option_with_value():
    cmd = Command(cmd="git commit")
    cmd.add_option("-m", "commit message")
    assert "-m" in cmd.list
    assert "commit message" in cmd.list


def test_command_params_mapping():
    cmd = Command(cmd="echo test", cwd="/testpath", shell=True, output=True)
    params = cmd.params
    assert params["args"] == "echo test"
    assert params["cwd"] == "/testpath"
    assert params["shell"] is True
    assert isinstance(params["timeout"], (int, float))
    assert params["text"] is True
    assert params["encoding"] == "utf-8"


def test_command_async_params_removes_timeout_and_check():
    cmd = Command(
        cmd="echo test",
        cwd="/tmp",
        shell=True,
        output=True,
        sync=False,
    )
    params = cmd.params
    assert params["args"] == "echo test"
    assert params["cwd"] == "/tmp"
    assert params["shell"] is True
    assert "timeout" not in params
    assert "check" not in params
    assert params["stdout"] is not None
    assert params["stderr"] is not None
