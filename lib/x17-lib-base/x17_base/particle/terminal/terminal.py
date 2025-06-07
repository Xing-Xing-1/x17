# -*- coding: utf-8 -*-
import os
import re
import shutil
import subprocess
from typing import Any, Dict, List, Optional, Union, Literal

import psutil
from x17_base.particle.datestamp import Datestamp
from x17_base.particle.duration import Duration
from x17_base.particle.platform import Platform
from x17_base.particle.terminal.command import Command
from x17_base.particle.terminal.process import Process
from x17_base.particle.terminal.processset import ProcessSet
from x17_base.particle.terminal.response import Response
from x17_base.particle.text import Text


class Terminal:

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

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "cwd": self.cwd,
            "env": self.env,
            "encoding": self.encoding,
            "platform": self.platform.name,
            "history": self.history,
        }

    def record(self, cmd: Command, response: Response) -> None:
        self.history.append({"command": cmd.dict, "response": response.dict})

    def run(
        self,
        cmd: Command,
        wait: Optional[Duration | int] = None,
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
        if isinstance(wait, int):
            wait = Duration(second=wait)
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

    # -- Check if program exists --

    @staticmethod
    def exist_from(
        program: Optional[str] = None,
        path: Optional[str] = None,
    ) -> bool:
        if program:
            return shutil.which(program) is not None
        elif path:
            return os.path.exists(path)

    def exist(
        self, 
        program: Optional[str] = None,
        path: Optional[str] = None,
    ) -> bool:
        if program:
            return Terminal.exist_from(program=program)
        elif path:
            return Terminal.exist_from(path=path)
        else:
            return False

    # -- Get version from program --

    @staticmethod
    def get_version_from(program: str, option: str = "--version") -> str:
        response = Terminal.run_from(
            cmd=Command(
                cmd=f"{program} {option}",
                check=True,
                shell=True,
            )
        )
        if response.success:
            match = re.search(r"\b\d+\.\d+(\.\d+)?\b", response.stdout)
            version = match.group(0) if match else ""
            return version
        else:
            return None

    def get_version(self, program: str, option: str = "--version") -> str:
        return Terminal.get_version_from(program=program, option=option)

    # -- Process management --

    @staticmethod
    def list_process_from() -> Optional[ProcessSet]:
        pool = ProcessSet()
        for proc in psutil.process_iter(ProcessSet.ALLOWED_OPTIONS):
            try:
                if proc.info.get("pid") is None:
                    continue
                process = Process.from_pid(proc.info.get("pid"))
                pool.add(process)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return pool

    def list_process() -> Optional[ProcessSet]:
        return Terminal.list_process_from()
    
    @staticmethod
    def find_process_from(
        keyword: str,
        attributes: Optional[List[str]] = None,
        ignore_case: bool = True,
        method: Literal["exact", "regex", "wildcard"] = None,
    ) -> Optional[ProcessSet]:
        if attributes is None:
            attributes = ProcessSet.ALLOWED_ATTRS
        
        pool = Terminal.list_process()
        if method == "regex":
            return pool.match_regex(
                keyword=keyword, 
                attributes=attributes, 
                ignore_case=ignore_case,
            )
        elif method == "wildcard":
            return pool.match_wildcard(
                keyword=keyword, 
                attributes=attributes, 
                ignore_case=ignore_case,
            )
        else:
            return pool.match(
                keyword=keyword, 
                attributes=attributes, 
                ignore_case=ignore_case,
            )
            
    def find_process(
        self,
        keyword: str,
        attributes: Optional[List[str]] = None,
        ignore_case: bool = True,
        method: Literal["", "regex", "wildcard"] = "",
    ) -> Optional[ProcessSet]:
        return Terminal.find_process_from(
            keyword=keyword,
            attributes=attributes,
            ignore_case=ignore_case,
            method=method,
        )

    @staticmethod
    def kill_process_from(
        keyword: str,
        attributes: Optional[List[str]] = None,
        ignore_case: bool = True,
        method: Literal["", "regex", "wildcard"] = "",
    ) -> Response:
        processes = Terminal.find_process_from(
            keyword=keyword,
            attributes=attributes,
            ignore_case=ignore_case,
            method=method,
        )
        for process in processes:
            process.kill()
        return [p.pid for p in processes]
        
        
    def kill_process(
        self,
        keyword: str,
        attributes: Optional[List[str]] = None,
        ignore_case: bool = True,
        method: Literal["", "regex", "wildcard"] = "",
    ) -> Response:
        return Terminal.kill_process_from(
            keyword=keyword,
            attributes=attributes,
            ignore_case=ignore_case,
            method=method,
        )