# -*- coding: utf-8 -*-

import os
import shlex
import subprocess
from typing import Any, Dict, List, Literal, Optional

from x17_base.particle.duration import Duration


class Command:
    """
    Command class to represent a command line instruction.
    It can be used to build command line arguments, manage environment variables,
    and handle command execution parameters.

    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Command":
        return cls(
            cmd=data.get("cmd"),
            cwd=data.get("cwd", None),
            env=data.get("env", None),
            shell=data.get("shell", None),
            check=data.get("check", True),
            timeout=(
                Duration.from_dict(data.get("timeout")) if data.get("timeout") else None
            ),
            encoding=data.get("encoding", "utf-8"),
            text=data.get("text", True),
            output=data.get("output", True),
            sync=data.get("sync", True),
        )

    def __init__(
        self,
        cmd: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, Any]] = None,
        shell: Optional[bool] = None,
        check: Optional[bool] = True,
        timeout: Optional[Duration] = None,
        encoding: str = "utf-8",
        text: Optional[bool] = True,
        output: Optional[bool] = True,
        sync: Optional[bool] = True,
    ) -> None:
        self.cmd = cmd if isinstance(cmd, str) else " ".join(cmd)
        self.cwd = cwd or os.getcwd()
        self.env = env or {}
        self.check = check
        self.shell = shell
        self.timeout = timeout or Duration(minute=2)
        self.encoding = encoding
        self.text = text
        self.output = output
        self.sync = sync

    @property
    def list(self) -> List[str]:
        if isinstance(self.cmd, list):
            return self.cmd
        else:
            return shlex.split(self.cmd)

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "cmd": self.cmd,
            "cwd": self.cwd,
            "env": self.env,
            "shell": self.shell,
            "check": self.check,
            "timeout": self.timeout.dict if self.timeout else None,
            "encoding": self.encoding,
            "text": self.text,
            "output": self.output,
            "sync": self.sync,
        }

    @property
    def params(
        self,
    ) -> Dict[str, Any]:
        base = {
            "args": self.cmd if self.shell else self.list,
            "cwd": self.cwd,
            "env": self.env,
            "shell": self.shell,
            "text": self.text,
            "encoding": self.encoding,
        }
        if self.sync:
            base.update(
                {
                    "timeout": self.timeout.base if self.timeout else None,
                    "check": self.check,
                }
            )
        else:
            base.update(
                {
                    "start_new_session": True,
                }
            )
        if self.output:
            base["stdout"] = subprocess.PIPE
            base["stderr"] = subprocess.PIPE
        return {k: v for k, v in base.items() if v is not None}

    def __str__(self) -> str:
        return " ".join(self.list)

    def __repr__(self) -> str:
        attributes = []
        for unit, value in self.dict.items():
            if value != 0:
                attributes.append(f"{unit}={value}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "cmd": self.cmd,
            "cwd": self.cwd,
            "env": self.env,
            "shell": self.shell,
            "check": self.check,
            "timeout": self.timeout.dict if self.timeout else None,
            "encoding": self.encoding,
            "text": self.text,
            "output": self.output,
            "sync": self.sync,
        }

    def add_option(self, option: str, value: Optional[str] = None) -> None:
        if value is not None:
            self.cmd += f" {option} {shlex.quote(value)}"
        else:
            self.cmd += f" {option}"

    def export(self) -> Dict[str, Any]:
        return self.dict
