# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, Tuple

from x17_base.particle.log import LogStream
from x17_base.particle.text import Id

class BaseModel():
    def __init__(
        self, 
        name: str,
        interface: Any = None,
        log_stream: Optional[Any] = None,
    ):
        """
        Initialize the model with the given name and any additional arguments.
        """
        self.name = name or f"{self.__class__.__name__}{Id.uuid(length=4)}"
        self.ready = False
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