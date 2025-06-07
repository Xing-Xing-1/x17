from typing import Optional, Dict, Any, List, Union

from x17_base.particle.terminal.command import Command
from x17_base.particle.terminal.terminal import Terminal
from x17_base.particle.terminal.response import Response
from x17_base.particle.terminal.process import Process
from x17_base.particle.terminal.processset import ProcessSet


class DaemonHandle:
    
    @classmethod
    def from_name(
        cls,
        name: str,
        start_command: Optional[str],
        stop_command: Optional[str],
        registries: Optional[Dict[str, Command]] = None,
    ) -> "DaemonHandle":
        start_command=Command(
            cmd=start_command, 
            shell=True, 
            sync=False,
        ) if start_command else None
        stop_command=Command(
            cmd=stop_command, 
            shell=True,
            sync=False,
        ) if stop_command else None
        return cls(
            name=name,
            start_command=start_command,
            stop_command=stop_command,
            strict=False,
            registries=registries,
        )
    
    def __init__(
        self,
        name: Optional[str],
        terminal: Optional[Terminal] = None,
        start_command: Optional[Command] = None,
        stop_command: Optional[Command] = None,
        strict: bool = False,
        registries: Optional[Dict[str, Command]] = None,
    ):
        self.name = name
        self.strict = strict
        self.start_command = start_command
        self.stop_command = stop_command
        self.terminal = terminal or Terminal()
        self.internal_processes = ProcessSet()
        self.registries = registries or {}

    @property
    def external_processes(self) -> ProcessSet:
        if self.strict:
            return ProcessSet()
        else:
            return self.terminal.find_process(
                keyword=self.name,
                attributes=["cmdline"],
                ignore_case=True,
                method="wildcard",
            )

    @property
    def all_processes(self) -> List[Process]:
        self.clear()
        return self.internal_processes + self.external_processes

    @property
    def is_available(self) -> bool:
        self.clear()
        return any(process.is_alive for process in self.all_processes)

    @property
    def spawned(self) -> List[Process]:
        self.clear()
        return [p for p in self.internal_processes if p.is_alive]

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "strict": self.strict,
            "is_available": self.is_available,
            "internal_count": len(self.internal_processes),
            "external_count": len(self.external_processes),
            "pids": [p.pid for p in self.all_processes],
            "version": self.get_version(),
            "registries": self.registries,
        }

    def __str__(self) -> str:
        return self.name
    
    def __bool__(self) -> bool:
        return self.is_available

    def __len__(self) -> int:
        return len(self.all_processes)

    def __repr__(self) -> str:
        attributes = []
        for unit, value in self.dict.items():
            if value:
                attributes.append(f"{unit}={value}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def start(
        self,
        command: Optional[Command] = None,
        wait: Optional[Union[int, float]] = None,
        force: bool = False,
    ) -> Response:
        if self.is_available and not force:
            return Response(
                success=False,
                message=f"{self.name} is already running.",
            )
        command = command or self.start_command
        response = self.terminal.run(command, wait=wait)
        if response.pid:
            proc = Process.from_pid(response.pid)
            if proc:
                self.internal_processes.add(proc)
            
        return response

    def restart(
        self,
        start_command: Optional[Command] = None,
        stop_command: Optional[Command] = None,
        wait: Optional[Union[int, float]] = None,
        force: bool = False,
    ) -> Response:
        if force:
            self.kill()
        else:
            self.stop(command=stop_command, wait=wait)
        return self.start(command=start_command, wait=wait, force=force)

    def run(
        self,
        command: Command,
        wait: Optional[Union[int, float]] = None,
    ) -> Response:
        return self.terminal.run(command, wait=wait)

    def stop(
        self,
        command: Optional[Command] = None,
        wait: Optional[Union[int, float]] = None,
        force: bool = False,
    ) -> Response:
        if not self.is_available and not force:
            return Response(
                success=False,
                message=f"{self.name} does not have active processes to stop.",
            )
        command = command or self.stop_command
        return self.terminal.run(command, wait=wait)

    def kill(self):
        seen = set()
        for process in self.all_processes:
            if process.is_alive and process.pid not in seen:
                process.kill()
                self.internal_processes.remove(process)
                seen.add(process.pid)
        return seen

    def clear(self):
        self.internal_processes = ProcessSet(
            [p for p in self.internal_processes if p.is_alive]
        )
    
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
    