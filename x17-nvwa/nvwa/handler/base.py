# -*- coding: utf-8 -*-
from typing import Dict, Any, Optional, List

from pangu.particle.log import LogStream


class BaseHandler():
    def __init__(
        self, 
        name: str = None,
        interface: Any = None,
        log_stream: Optional[LogStream] = None,
    ):
        self.name = name or f"{self.__class__.__name__}"
        self.interface = interface
        self.log_stream = log_stream or LogStream(
            name=f"{self.name}LogStream", 
            group=interface.log_group if interface else None,
        )
    
    def log(
        self, 
        message: str, 
        level: str = "info",
        context: Optional[str] = None,
        code: Optional[int] = None,
        tags: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Log a message to the log stream.
        Using predefined log mechanism to distribute log messages.
        """
        self.log_stream.log(
            message=message,
            level=level,
            context=context,
            code=code,
            tags=tags,
            metrics=metrics,
            **kwargs,
        )