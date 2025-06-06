from typing import Optional, Dict, Any, Union
from pangu.particle.terminal.command import Command
from pangu.particle.terminal.terminal import Terminal
from pangu.particle.terminal.response import Response
from pangu.particle.platform import Platform

class ServiceHandle:
    
    def from_name(
        cls,
        name: str,
    ) -> "ServiceHandle":
        return cls(
            name=name,
        )
    
    def __init__(
        self,
        name: str,
        registries: Optional[Dict[str, Command]] = None,
        terminal: Optional[Terminal] = None,
        exact: bool = False,
    ):
        self.name = name
        self.exact = exact
        self.registries = registries or {}
        self.terminal = terminal or Terminal()
        self.platform = Platform()

    @property
    def is_available(self) -> bool:
        if self.exact:
            processes = self.terminal.find_process(
                name=self.name,
            )
        else:
            processes = self.terminal.find_process(
                keyword=f"*{self.name}*",
                method="wildcard"
            )
        return len(processes) > 0

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "is_available": self.is_available,
            "registries": self.registries,
        }

    def __bool__(self) -> bool:
        return self.is_available

    def __str__(self) -> str:
        return self.name

    def __len__(self) -> int:
        return 1 if self.is_available else 0

    def __repr__(self) -> str:
        attributes = []
        for key, val in self.dict.items():
            if val:
                attributes.append(f"{key}={val}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def run(
        self,
        command: Command,
        wait: Optional[Union[int, float]] = None,
    ) -> Response:
        return self.terminal.run(command, wait=wait)

    def get_version(
        self,
        **kwargs: Any,
    ) -> Optional[str]:
        return "Not Supported"

    def register(
        self,
        label: str,
        command: Command,
        as_method: bool = False,
    ) -> None:
        if label in self.registries:
            raise ValueError(f"Label '{label}' is already registered.")
        self.registries[label] = command
        
        if as_method:
            if hasattr(self, label):
                raise ValueError(f"Method '{label}' already exists.")
            else:
                def bound_method(_command=command):
                    return self.run(_command)
                setattr(self, label, bound_method)
        
    def get_registered(
        self,
        label: str,
    ) -> Optional[Command]:
        return self.registries.get(label)