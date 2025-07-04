#!/usr/bin/python
# -*- coding: utf-8 -*-
import queue
import threading
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from x17_base.particle.log.log_event import LogEvent
from x17_base.particle.text.id import Id

if TYPE_CHECKING:
    from x17_base.particle.log.log_group import LogGroup


class LogCore:
    def __init__(
        self,
        name: Optional[str] = "",
    ):
        self.id = Id.uuid(8)
        self.base_name = name
        self.name = name or f"{self.__class__.__name__}:{self.id}"
        self.groups: Dict[str, Dict[str, List[LogEvent]]] = {}
        self.queue: queue.Queue = queue.Queue()
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._consume, daemon=True)
        self._thread.start()

    @property
    def attr(self) -> list[str]:
        return [
            key for key in self.__dict__.keys() 
            if not key.startswith("_") and isinstance(self.__dict__[key], str)
        ]

    @property
    def dict(self) -> dict[str, str]:
        return {key: getattr(self, key) for key in self.attr}

    def __repr__(self):
        attr_parts = []
        for key in self.attr:
            value = getattr(self, key, None)
            attr_parts.append(f"{key}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(attr_parts)})"

    def __str__(self):
        return self.name

    def register_group(self, group: "LogGroup") -> str:
        with self._lock:
            self.groups.setdefault(group.name, {})
        group.core = self
        return group.name

    def push(self, group: str, stream: str, event: LogEvent):
        self.queue.put((group, stream, event))

    def _consume(self):
        while True:
            group, stream, event = self.queue.get()
            with self._lock:
                self.groups.setdefault(group, {}).setdefault(stream, []).append(event)

    def export(self, group: Optional[str] = None, stream: Optional[str] = None) -> Any:
        with self._lock:
            if group is None:
                return {
                    g: {s: [e.export() for e in streams] for s, streams in grp.items()}
                    for g, grp in self.groups.items()
                }
            if stream is None:
                return {
                    s: [e.export() for e in self.groups.get(group, {}).get(s, [])]
                    for s in self.groups.get(group, {})
                }
            return [e.export() for e in self.groups.get(group, {}).get(stream, [])]
