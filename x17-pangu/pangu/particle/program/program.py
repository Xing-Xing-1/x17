from typing import Optional, Dict, Any, Union
from pangu.particle.programhandle.cli import CliHandle
from pangu.particle.programhandle.daemon import DaemonHandle
from pangu.particle.programhandle.web import WebHandle
from pangu.particle.programhandle.gui import GuiHandle
from pangu.particle.programhandle.service import ServiceHandle

class Program:
    def __init__(
        self,
        name: str,
        cli: Optional[CliHandle] = None,
        daemon: Optional[DaemonHandle] = None,
        web: Optional[WebHandle] = None,
        gui: Optional[GuiHandle] = None,
        service: Optional[ServiceHandle] = None,
    ):
        self.name = name
        self.handles = {
            "cli": cli,
            "daemon": daemon,
            "web": web,
            "gui": gui,
            "service": service,
        }

    @property
    def is_available(self) -> bool:
        return any([
            handle.is_available if handle else False
            for handle in self.handles.values()
        ])

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "handles": {
                handle_name: handle.dict if handle else None
                for handle_name, handle in self.handles.items()
            },
        }

    def __str__(self) -> str:
        return f"Program({self.name})"

    def __repr__(self) -> str:
        return f"Program(name={self.name}, available={self.is_available})"

    def __bool__(self) -> bool:
        return self.is_available