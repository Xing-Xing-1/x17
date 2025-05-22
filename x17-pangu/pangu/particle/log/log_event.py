#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pangu.particle.datestamp import Datestamp
from pangu.particle.text.id import Id


class LogEvent:
    
    def from_dict(
        self,
        data: Dict[str, Any],
    ) -> LogEvent:
        return LogEvent(
            message=data.get("message", ""),
            level=data.get("level", "INFO"),
            datestamp=data.get("datestamp", None),
        )

    def __init__(
        self,
        message: str,
        name: Optional[str] = "",
        level: str = "INFO",
        datestamp: Optional[Datestamp] = None,
        context: Optional[str] = None,
        code: Optional[int] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ):
        self.id = Id.uuid(5)
        self.base_name = name
        self.name = f"{name}:{self.id}" or f"{self.__class__.__name__}:{self.id}"
        if isinstance(datestamp, Datestamp):
            self.datestamp = datestamp.datestamp_str
            self.time_zone_name = datestamp.time_zone_name
        else:
            self.datestamp = Datestamp.now().datestamp_str
            self.time_zone_name = Datestamp.now().time_zone_name
            
        self.level = level.upper()
        self.message = message
        self.context = context
        self.code = code
        self.tags = tags or []
        self.metrics = metrics or {}
        self.extra = extra or {}
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def attr(self) -> list[str]:
        return [
            key for key in self.__dict__.keys() 
            if not key.startswith("_")
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
    
    def export(self) -> Dict[str, str]:
        return self.dict
