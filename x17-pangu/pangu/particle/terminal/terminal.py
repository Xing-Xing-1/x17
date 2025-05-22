# -*- coding: utf-8 -*-
import shutil
import os
import re
import psutil
import subprocess
from typing import Any, Dict, Optional

from pangu.particle.terminal.command import Command
from pangu.particle.terminal.response import Response
from pangu.particle.datestamp import Datestamp
from pangu.particle.duration import Duration
from pangu.particle.platform import Platform

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
        
        
    # -- Check if program exists --
        
    @staticmethod
    def exist_from(program) -> bool:
        return shutil.which(program) is not None
        
    def exist(self, program: str) -> bool:
        return Terminal.exist_from(program=program)
    
    
    # -- Get version from program -- 
    
    
    @staticmethod
    def get_version_from(program: str, option: str = "--version") -> str:
        response = Terminal.run_from(
            cmd=Command(cmd=f"{program} {option}", check=True, shell=True,)
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
    
    # @staticmethod
    # def list_process_from(keyword: str = None) -> Optional[str]:
    #     results = []
    #     for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'username', 'cpu_percent', 'memory_percent']):
        
    #     response = Terminal.run_from(cmd=Command(cmd=cmd, shell=True))
    #     if response.success and response.stdout.strip():
    #         return response.stdout.strip()
    #     return None
    # # psutil
    
    # def list_processes_structured(self) -> List[Dict[str, Any]]:
    #     results = []
    #     for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'username', 'cpu_percent', 'memory_percent']):
    #         try:
    #             results.append(proc.info)
    #         except (psutil.NoSuchProcess, psutil.AccessDenied):
    #             continue
    #     return results

    # def find_process(self, keyword: str) -> bool:
    #     for proc in psutil.process_iter(['cmdline']):
    #         try:
    #             cmd = " ".join(proc.info['cmdline'] or [])
    #             if keyword in cmd:
    #                 return True
    #         except (psutil.NoSuchProcess, psutil.AccessDenied):
    #             continue
    #     return False

    # def kill_process(self, keyword: str) -> List[int]:
    #     killed = []
    #     for proc in psutil.process_iter(['pid', 'cmdline']):
    #         try:
    #             cmd = " ".join(proc.info['cmdline'] or [])
    #             if keyword in cmd:
    #                 proc.kill()
    #                 killed.append(proc.info['pid'])
    #         except (psutil.NoSuchProcess, psutil.AccessDenied):
    #             continue
    #     return killed
    