from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pangu.particle.log.log_event import LogEvent
from pangu.particle.text.id import Id

if TYPE_CHECKING:
    from pangu.particle.log.log_group import LogGroup


class LogStream:
    
    def __init__(
        self,
        name: Optional[str] = "",
        group: Optional[LogGroup] = None,
        format: Optional[str] = None,
        verbose: Optional[bool] = False,
    ):
        self.id = Id.uuid(8)
        self.base_name = name
        self.name = name or f"{self.__class__.__name__}:{self.id}"
        self.group = group or None
        self.log_format = format or "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
        self.log_node = self._setup_node()
        self.verbose = verbose
        self.memory = []

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
    
    def _setup_node(self):
        log_node = logging.getLogger(f"LogStream:{self.name}")
        if not log_node.handlers:
            log_node.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter(self.log_format)
            handler.setFormatter(formatter)
            log_node.addHandler(handler)
        return log_node

    def log(
        self,
        message: str,
        name: Optional[str] = None,
        level: str = "INFO",
        datestamp: Optional[str] = None,
        context: Optional[str] = None,
        code: Optional[int] = None,
        tags: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        event = LogEvent(
            message=message,
            level=level,
            datestamp=datestamp,
            name=name or self.name,
            context=context,
            code=code,
            tags=tags,
            metrics=metrics,
            extra=extra,
            **kwargs,
        )
        if self.group:
            self.group.receive(self.name, event)
        else:
            self.memory.append(event)

        if self.verbose:
            self.log_node.log(
                getattr(logging, level.upper(), logging.INFO),
                message,
            )

    def info(
        self,
        message: str,
        name: Optional[str] = None,
        datestamp: Optional[str] = None,
        context: Optional[str] = None,
        code: Optional[int] = None,
        tags: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.log(
            message=message,
            level="INFO",
            name=name,
            datestamp=datestamp,
            context=context,
            code=code,
            tags=tags,
            metrics=metrics,
            extra=extra,
            **kwargs,
        )

    def error(
        self,
        message: str,
        name: Optional[str] = None,
        datestamp: Optional[str] = None,
        context: Optional[str] = None,
        code: Optional[int] = None,
        tags: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.log(
            message=message,
            level="ERROR",
            name=name,
            datestamp=datestamp,
            context=context,
            code=code,
            tags=tags,
            metrics=metrics,
            extra=extra,
            **kwargs,
        )
    
    def warn(
        self,
        message: str,
        name: Optional[str] = None,
        datestamp: Optional[str] = None,
        context: Optional[str] = None,
        code: Optional[int] = None,
        tags: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.log(
            message=message,
            level="WARN",
            name=name,
            datestamp=datestamp,
            context=context,
            code=code,
            tags=tags,
            metrics=metrics,
            extra=extra,
            **kwargs,
        )
    
    def critical(
        self,
        message: str,
        name: Optional[str] = None,
        datestamp: Optional[str] = None,
        context: Optional[str] = None,
        code: Optional[int] = None,
        tags: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.log(
            message=message,
            level="CRITICAL",
            name=name,
            datestamp=datestamp,
            context=context,
            code=code,
            tags=tags,
            metrics=metrics,
            extra=extra,
            **kwargs,
        )
       
    def debug(
        self,
        message: str,
        name: Optional[str] = None,
        datestamp: Optional[str] = None,
        context: Optional[str] = None,
        code: Optional[int] = None,
        tags: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.log(
            message=message,
            level="DEBUG",
            name=name,
            datestamp=datestamp,
            context=context,
            code=code,
            tags=tags,
            metrics=metrics,
            extra=extra,
            **kwargs,
        )
    
    def export(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "group": self.group.name if self.group else None,
            "log_format": self.log_format,
            "verbose": self.verbose,
            "logs": [event.export() for event in self.memory],
        }