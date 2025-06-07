from typing import Union, Any, Dict, Optional, List
from x17_base.particle.terminal.command import Command
from x17_base.particle.terminal.terminal import Terminal
from x17_base.particle.terminal.response import Response

class CliHandle:
    
    @classmethod
    def from_name(
        cls,
        name: str,
        registries: Optional[Dict[str, Command]] = None,
    ) -> "CliHandle":
        return cls(
            name=name,
            registries=registries or {},
        )
    
    def __init__(
        self, 
        name: str,
        terminal: Optional[Terminal] = None,
        registries: Optional[Dict[str, Command]] = None,
    ):
        self.name = name
        self.terminal = terminal or Terminal()
        self.registries = registries or {}

    @property
    def is_available(self) -> bool:
        return self.terminal.exist(self.name)
    
    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "is_available": self.is_available,
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
        option: str = "--version",
    ) -> Optional[str]:
        return Terminal.get_version_from(program=self.name, option=option)
    
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
    