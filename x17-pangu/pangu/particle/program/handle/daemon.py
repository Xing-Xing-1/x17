from typing import Optional, Dict, Any, List, Union
from pangu.particle.terminal.command import Command
from pangu.particle.terminal.terminal import Terminal
from pangu.particle.terminal.response import Response

class DaemonHandle:
    def __init__(
        self,
        cmd: Union[str, List[str]],
        keyword: Optional[str] = None,
        terminal: Optional[Terminal] = None,
    ):
        self.cmd = cmd if isinstance(cmd, str) else " ".join(cmd)
        self.keyword = keyword or self.cmd.split()[0]
        self.terminal = terminal or Terminal()

    def is_running(self) -> bool:
        if self.terminal.is_macos or self.terminal.is_linux:
            check_cmd = Command(cmd=f"pgrep -f '{self.keyword}'", shell=True)
        elif self.terminal.is_windows:
            check_cmd = Command(cmd=f'tasklist | findstr /i "{self.keyword}"', shell=True)
        else:
            return False
        result = self.terminal.run(check_cmd)
        return result.success and result.stdout.strip() != ""

    def start(self, wait: int = 0) -> Response:
        command = Command(cmd=self.cmd, shell=True, sync=False)
        return self.terminal.run(command, wait=wait)

    def __str__(self) -> str:
        return self.keyword

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(cmd={self.cmd})"

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "cmd": self.cmd,
            "keyword": self.keyword,
            "terminal": self.terminal.dict if self.terminal else None,
        }
        
    def stop(self) -> Response:
        if self.terminal.is_macos or self.terminal.is_linux:
            cmd = Command(cmd=f"pkill -f '{self.keyword}'", shell=True)
        elif self.terminal.is_windows:
            cmd = Command(cmd=f'taskkill /F /IM {self.keyword}', shell=True)
        else:
            return Response(code=500, stderr="Unsupported OS", stdout="", cmdline="")
        return self.terminal.run(cmd)
