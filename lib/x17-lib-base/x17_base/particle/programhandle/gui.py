from typing import Union, Any, Dict, Optional, List
from x17_base.particle.terminal.command import Command
from x17_base.particle.terminal.terminal import Terminal
from x17_base.particle.terminal.response import Response
from x17_base.particle.platform import Platform
import os

class GuiHandle:
    
    @classmethod
    def from_path(
        cls, 
        path: str, 
        name: Optional[str] = None,
    ) -> "GuiHandle":
        return cls(
            name=name or os.path.basename(path), 
            path=path,
        )
        
    def __init__(
        self, 
        name: str,
        path: Optional[str] = None,
        registries: Optional[Dict[str, Command]] = None,
        terminal: Optional[Terminal] = None,
    ):
        self.name = name
        self.path = path
        self.registries = registries or {}
        self.terminal = terminal or Terminal()
        self.platform = Platform()

    @property
    def is_available(self) -> bool:
        return self.terminal.exist(
            path=self.path or self.name,
        )
    
    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "is_available": self.is_available,
            "registries": self.registries,
        }
    
    def __bool__(self) -> bool:
        return self.is_available

    def __str__(self) -> str:
        return self.name
    
    def __len__(self) -> int:
        if self.is_available:
            return 1
        else:
            return 0
    
    def __repr__(self) -> str:
        attributes = []
        for unit, value in self.dict.items():
            if value != 0:
                attributes.append(f"{unit}={value}")
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