from typing import Union, Any, Dict, Optional, List, Literal
from pangu.particle.terminal.command import Command
from pangu.particle.terminal.terminal import Terminal
from pangu.particle.terminal.response import Response

class CLIHandle:
    def __init__(
        self, 
        name: str,
        terminal: Optional[Terminal] = Terminal()
    ):
        self.name = name
        self.terminal = terminal

    def is_available(self) -> bool:
        return self.terminal.exist(self.name)

    def run(
        self,
        args: Union[str, List[str]] = "",
        cwd: Optional[str] = None,
        env: Optional[Dict[str, Any]] = None,
        shell: Optional[bool] = None,
        check: Optional[bool] = True,
        timeout: Optional[Union[int, float]] = None,
        encoding: str = "utf-8",
        text: Optional[bool] = True,
        output: Optional[bool] = True,
        sync: Optional[bool] = True,
        wait: Optional[Union[int, float]] = None,
    ) -> Response:
        args = args if isinstance(args, str) else " ".join(args)
        command = Command(
            cmd = f"{self.name} {args}".strip(),
            cwd = cwd,
            env = env,
            shell = shell,
            check = check,
            timeout = timeout,
            encoding = encoding,
            text = text,
            output = output,
            sync = sync,
        )
        response = self.terminal.run(command, wait = wait)
        return response

    def get_version(self, option: str = "--version") -> str:
        return self.terminal.get_version(program=self.name, option=option)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
    
    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "terminal": self.terminal.dict if self.terminal else None,
        }