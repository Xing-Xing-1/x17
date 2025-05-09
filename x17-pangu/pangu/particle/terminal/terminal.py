# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from typing import Any, Dict, Optional

from pangu.particle.terminal.command import Command
from pangu.particle.terminal.response import Response
from pangu.particle.datestamp import Datestamp


class Terminal:
    """
    A cross-platform virtual Terminal.
    """

    def __init__(
        self,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        encoding: str = "utf-8",
    ):
        self.cwd = cwd
        self.env = env
        self.encoding = encoding
        self.history = []

    @property
    def is_windows(self) -> bool:
        return sys.platform.startswith("win")

    @property
    def is_macos(self) -> bool:
        return sys.platform.startswith("darwin")

    @property
    def is_linux(self) -> bool:
        return sys.platform.startswith("linux")

    def run(self, cmd: Command) -> Response:
        """
        Run a command using the instance's cwd/env/encoding.
        """
        response = Terminal.run_from(
            cmd=cmd,
            cwd=cmd.cwd or self.cwd or os.getcwd(),
            env=cmd.env or self.env or os.environ.copy(),
            encoding=cmd.encoding or self.encoding,
        )
        self.record(cmd, response)
        return response

    @staticmethod
    def run_from(
        cmd: Command,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        encoding: str = "utf-8",
    ) -> Response:
        """
        Stateless command execution, used as the primary logic.
        """
        start = Datestamp.now()
        params = cmd.params.copy()
        params["cwd"] = cwd or os.getcwd()
        params["env"] = env or os.environ.copy()
        params["encoding"] = encoding

        try:
            result = subprocess.run(**params)
            end = Datestamp.now()
            return Response.from_object(
                obj=result,
                started=start,
                ended=end,
                cwd=params["cwd"],
                env=params["env"],
                captured=True,
            )
        except subprocess.TimeoutExpired:
            end = Datestamp.now()
            return Response(
                code=-1,
                stdout="",
                stderr=f"Timeout after {params.get('timeout')} seconds",
                started=start,
                ended=end,
                cwd=params["cwd"],
                env=params["env"],
                cmdline=" ".join(cmd.list),
                captured=True,
                signal=None,
            )
        except Exception as e:
            end = Datestamp.now()
            return Response(
                code=-1,
                stdout="",
                stderr=str(e),
                started=start,
                ended=end,
                cwd=params["cwd"],
                env=params["env"],
                cmdline=" ".join(cmd.list),
                captured=True,
                signal=None,
            )

    def record(self, cmd: Command, response: Response) -> None:
        self.history.append({
            "command": cmd.dict,
            "response": response.dict,
        })
        
    def exist(
        self,
        program: str = None,
    ) -> bool:
        if (program):
            return Terminal.exist_from(program=program)

    @staticmethod
    def exist_from(
        program: str = None,
    ) -> bool:
        if (program):
            cmd = Command(cmd=f"which {program}")
            result = Terminal.run_from(cmd)
            return result.clean_success
        