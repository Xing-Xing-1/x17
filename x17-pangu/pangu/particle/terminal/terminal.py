# -*- coding: utf-8 -*-
import shutil
import os
import subprocess
from typing import Any, Dict, Optional

from pangu.particle.terminal.command import Command
from pangu.particle.terminal.response import Response
from pangu.particle.datestamp import Datestamp
from pangu.particle.duration import Duration
from pangu.particle.platform import Platform

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
        self.platform = Platform()
        self.history = []

    @property
    def is_windows(self) -> bool:
        return self.platform.is_windows

    @property
    def is_macos(self) -> bool:
        return self.platform.is_macos
    
    @property
    def is_linux(self) -> bool:
        return self.platform.is_linux

    def run(
        self, 
        cmd: Command,
        wait: Optional[Duration | int] = Duration(second=5),
    ) -> Response:
        cmd.env = {
            **os.environ,
            **(self.env or {}),
            **(cmd.env or {}),
        }
        if cmd.sync:
            response = Terminal.run_from_sync(cmd=cmd, wait=wait)
        else:
            response = Terminal.run_from_async(cmd=cmd, wait=wait)
        self.record(cmd, response)
        return response

    @staticmethod
    def run_from(
        cmd: Command, 
        wait: Optional[Duration | int] = None,
    ) -> Response:            
        if cmd.sync:
            return Terminal.run_from_sync(cmd=cmd, wait=wait)
        else:
            return Terminal.run_from_async(cmd=cmd, wait=wait)

    @staticmethod
    def run_from_sync(
        cmd: Command,
        wait: Optional[Duration | int] = None,
    ) -> Response:
        """
        Synchronously run a command and capture its output.
        """
        start = Datestamp.now()
        params = cmd.params.copy()
        
        try:
            result = subprocess.run(**params)
            if wait and wait.base > 0: 
                wait.wait()
            end = Datestamp.now()
            return Response(
                code=result.returncode,
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                started=start,
                ended=end,
                cwd=params.get("cwd"),
                env=params.get("env"),
                cmdline=str(cmd),
                captured=True,
                sync=True,
                pid=None,
                process=None,
            )
        except Exception as e:
            end = Datestamp.now()
            return Response(
                code=500,
                stdout="",
                stderr=str(e),
                started=start,
                ended=end,
                cwd=params.get("cwd"),
                env=params.get("env"),
                cmdline=str(cmd),
                captured=False,
                sync=True,
                pid=None,
                process=None,
            )
        
    @staticmethod
    def run_from_async(
        cmd: Command, 
        wait: Optional[Duration | int] = None,
    ) -> Response:
        """
        Asynchronously launch a command (non-blocking).
        """
        if isinstance(wait, int): wait = Duration(second=wait)
        start = Datestamp.now()
        params = cmd.params.copy()
        try:
            process = subprocess.Popen(**params)
            if wait and wait.base > 0: 
                wait.wait()
            end = Datestamp.now()
            return Response(
                code=0,
                stdout="",
                stderr="",
                started=start,
                ended=end,
                cwd=params.get("cwd"),
                env=params.get("env"),
                cmdline=str(cmd),
                captured=False,
                sync=False,
                pid=process.pid,
                process=process,
            )
        except Exception as e:
            end = Datestamp.now()
            return Response(
                code=500,
                stdout="",
                stderr=str(e),
                started=start,
                ended=end,
                cwd=params.get("cwd"),
                env=params.get("env"),
                cmdline=str(cmd),
                captured=False,
                sync=False,
                pid=None,
                process=None,
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
        return shutil.which(program) is not None
        
    