# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional

import psutil
from pangu.particle.datestamp import Datestamp
from pangu.particle.duration import Duration
from pangu.particle.text import Text
from psutil import Process as PsutilProcess


class Process:

    @classmethod
    def from_pid(
        cls,
        pid: int,
    ) -> Optional["Process"]:
        try:
            proc = PsutilProcess(pid)
            return cls.from_object(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    @classmethod
    def from_object(
        cls,
        proc: PsutilProcess,
    ) -> Optional["Process"]:
        try:
            return cls(proc=proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def __init__(
        self,
        proc: PsutilProcess = None,
    ):
        self.proc = proc or PsutilProcess()
        self.pid = proc.pid
        self.gid = self._safe_call(self.proc.gids, None)
        self.uid = self._safe_call(self.proc.uids, None)
        self.name = self._safe_call(self.proc.name, "")
        self.status = self._safe_call(self.proc.status, "unknown")
        self.cmd = self._safe_call(self.proc.cmdline, [])
        self.cmdline = Text(" ".join(self.cmd)) if self.cmd else Text("")
        self.username = self._safe_call(self.proc.username, "")
        self.env = self._safe_call(self.proc.environ, {})
        self.cwd = self._safe_call(self.proc.cwd, "")
        self.exe = self._safe_call(self.proc.exe, "")
        self.create_timestamp = self._safe_call(self.proc.create_time, None)
        self.create_datestamp = (
            Datestamp.from_timestamp(
                self.create_timestamp,
            )
            if self.create_timestamp
            else None
        )
        self.parent_pid = self._safe_call(self.proc.ppid, None)
        self.num_threads = self._safe_call(self.proc.num_threads, 0)
        self.priority = self._safe_call(self.proc.nice, 0)
        self.cpu_percent = self._safe_call(self.proc.cpu_percent, 0.0)
        self.memory_percent = self._safe_call(self.proc.memory_percent, 0.0)

    @staticmethod
    def _safe_call(callable, default=None) -> Any:
        try:
            return callable()
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            return default

    @property
    def attr(self) -> list[str]:
        return [
            key
            for key in self.__dict__.keys()
            if not key.startswith("_") and key not in ["proc"]
        ]

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            key: str(getattr(self, key))
            for key in self.attr
            if hasattr(self, key) and not callable(getattr(self, key))
        }

    def __repr__(self) -> str:
        attributes = []
        for unit, value in self.dict.items():
            if value:
                attributes.append(f"{unit}={value[0:50]}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def __str__(self) -> str:
        return f"{self.pid}"

    @property
    def is_zombie(self) -> bool:
        return self.status.lower() == "zombie"

    @property
    def memory_info(self) -> Dict[str, Any]:
        memory_info = self._safe_call(self.proc.memory_info, None)
        if memory_info is None:
            return {}
        else:
            return {
                "rss": memory_info.rss,
                "vms": memory_info.vms,
            }

    @property
    def is_running(self) -> bool:
        return self.proc.is_running() if self.proc else False
    
    @property
    def is_alive(self) -> bool:
        return self.is_running and not self.is_zombie

    @property
    def is_root(self) -> bool:
        return self.username.lower() == "root"

    @property
    def is_system(self) -> bool:
        return self.username.lower() == "system"

    def get_cpu_times(self) -> Dict[str, float]:
        try:
            times = self.proc.cpu_times()
            return {
                "user": times.user,
                "system": times.system,
                "children_user": times.children_user,
                "children_system": times.children_system,
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {}

    def get_open_files(self) -> Dict[str, int]:
        try:
            return {
                f.path: f.fd
                for f in self.proc.open_files()
                if f.path and f.fd is not None
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {}

    def get_threads(self) -> List[Dict[str, Any]]:
        try:
            threads = self.proc.threads()
            return [
                {
                    "id": thread.id,
                    "user_time": thread.user_time,
                    "system_time": thread.system_time,
                }
                for thread in threads
            ]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []

    def get_connections(self) -> List[Dict[str, Any]]:
        try:
            connections = self.proc.net_connections()
            return [
                {
                    "fd": conn.fd,
                    "family": conn.family.name,
                    "type": conn.type.name,
                    "laddr": conn.laddr,
                    "raddr": conn.raddr,
                    "status": conn.status,
                }
                for conn in connections
            ]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []

    def get_children(
        self,
        recursive: bool = False,
        include_zombies: bool = False,
    ) -> List["Process"]:
        try:
            children = self.proc.children(recursive=recursive)
            if not include_zombies:
                children = [child for child in children if not child.is_zombie]
            return [Process.from_object(child) for child in children]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []

    def kill(
        self, 
        safenet: Optional[int] = 1,
        timeout: Optional[float | Duration] = Duration(second=5),
    ) -> bool:
        if self.pid == 0:
            Warning("Cannot kill process with PID 0 (init/system process).")
            return False
        if self.pid <= safenet:
            Warning(f"Cannot kill process with PID {self.pid} where safenet is set to {safenet}(system process).")
            return False
        if isinstance(timeout, int or float):
            timeout = Duration(second=timeout)
        try:
            self.proc.kill()
            self.wait(timeout=timeout.base)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            Warning(f"Failed to kill process {self.pid}. It may not exist or you do not have permission.")
            return False

    def terminate(
        self,
        safenet: Optional[int] = 1,
        timeout: Optional[float | Duration] = Duration(second=5),
    ) -> bool:
        if self.pid == 0:
            Warning("Cannot kill process with PID 0 (init/system process).")
            return False
        if self.pid <= safenet:
            Warning(f"Cannot kill process with PID {self.pid} where safenet is set to {safenet}(system process).")
            return False
        if isinstance(timeout, int or float):
            timeout = Duration(second=timeout)
        try:
            self.proc.terminate()
            self.wait(timeout=timeout.base)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            Warning(f"Failed to kill process {self.pid}. It may not exist or you do not have permission.")
            return False

    def resume(
        self,
        timeout: Optional[float | Duration] = Duration(second=5),
    ) -> bool:
        if isinstance(timeout, int or float):
            timeout = Duration(second=timeout)
        try:
            self.proc.resume()
            self.wait(timeout=timeout.base)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            Warning(f"Failed to suspend process {self.pid}. It may not exist or you do not have permission.")
            return False
        
    def suspend(
        self,
        timeout: Optional[float | Duration] = Duration(second=5),
    ) -> bool:
        if isinstance(timeout, int or float):
            timeout = Duration(second=timeout)
        try:
            self.proc.suspend()
            self.wait(timeout=timeout.base)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            Warning(f"Failed to suspend process {self.pid}. It may not exist or you do not have permission.")
            return False

    def wait(
        self,
        timeout: Optional[float | Duration] = Duration(second=5),
    ) -> bool:
        if isinstance(timeout, int or float):
            timeout = Duration(second=timeout)
        try:
            self.proc.wait(timeout=timeout.base)
            return True
        except (psutil.NoSuchProcess, psutil.TimeoutExpired):
            Warning(f"Process {self.pid} did not complete within the timeout period.")
            return False