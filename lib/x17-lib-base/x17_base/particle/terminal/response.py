# -*- coding: utf-8 -*-
import subprocess
from typing import Any, Dict, Optional

from x17_base.particle.datestamp import Datestamp
from x17_base.particle.duration import Duration


class Response:
    """
    Represents the result of a Terminal command execution (Extended Version).

    """

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "Response":
        return cls(
            code=data.get("code"),
            stdout=data.get("stdout", ""),
            stderr=data.get("stderr", ""),
            started=Datestamp.from_string(
                string=data["started"], time_zone_name=data.get("started_tz")
            ),
            ended=Datestamp.from_string(
                string=data["ended"], time_zone_name=data.get("ended_tz")
            ),
            cwd=data.get("cwd"),
            env=data.get("env"),
            cmdline=data.get("cmdline"),
            captured=data.get("captured", True),
            signal=data.get("signal"),
            sync=data.get("sync", False),
            process=data.get("process"),
            pid=data.get("pid"),
        )

    @classmethod
    def from_object(
        cls,
        obj: Any,
        started: Datestamp,
        ended: Datestamp,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        captured: bool = True,
    ) -> "Response":
        return cls(
            code=getattr(obj, "returncode"),
            stdout=getattr(obj, "stdout", "") or "",
            stderr=getattr(obj, "stderr", "") or "",
            started=started,
            ended=ended,
            cwd=cwd,
            env=env,
            cmdline=" ".join(obj.args) if hasattr(obj, "args") else None,
            captured=captured,
            signal=None,
        )

    def __init__(
        self,
        code: int,
        stdout: str,
        stderr: str,
        started: Datestamp = Datestamp.now(),
        ended: Datestamp = Datestamp.now(),
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        cmdline: Optional[str] = None,
        captured: bool = True,
        signal: Optional[int] = None,
        sync: Optional[bool] = False,
        process: Optional[subprocess.Popen] = None,
        pid: Optional[int] = None,
    ):
        self.code = code
        self.stdout = stdout.strip()
        self.stderr = stderr.strip()
        self.started = started
        self.ended = ended
        self.cwd = cwd
        self.env = env
        self.cmdline = cmdline
        self.captured = captured
        self.signal = signal
        self.duration = ended - started
        self.sync = sync
        self.process = process
        self.pid = pid

    @property
    def success(self) -> bool:
        return self.code == 0

    @property
    def clean_success(self) -> bool:
        return (
            self.code == 0
            and bool(self.stdout)
            and not self.stderr
            and not self.timeout
        )

    @property
    def failed(self) -> bool:
        return not self.success

    @property
    def timeout(self) -> bool:
        # 9=SIGKILL, 15=SIGTERM
        return self.code == -1 or (self.signal in (9, 15))

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "started": self.started.datestamp_str,
            "started_tz": self.started.time_zone_name,
            "ended": self.ended.datestamp_str,
            "ended_tz": self.ended.time_zone_name,
            "duration": self.duration.base,
            "cwd": self.cwd,
            "env": self.env,
            "cmdline": self.cmdline,
            "captured": self.captured,
            "signal": self.signal,
            "sync": self.sync,
            "pid": self.pid,
        }

    def __str__(self) -> str:
        return self.stdout or self.stderr or ""

    def __repr__(self) -> str:
        attributes = []
        for unit, value in self.dict.items():
            attributes.append(f"{unit}={value}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def export(self) -> Dict[str, Any]:
        return dict(self.dict)
