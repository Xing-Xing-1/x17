# -*- coding: utf-8 -*-
from typing import Dict, Any, Optional, List

from x17_base.particle.log import LogStream
from x17_base.particle.text import Id


class BaseHandler():
    def __init__(
        self, 
        name: str = None,
        interface: Any = None,
        log_stream: Optional[LogStream] = None,
        verbose: bool = True,
    ):
        self.name = name or f"{self.__class__.__name__}{Id.uuid(length=4)}"
        self.interface = interface
        self.verbose = getattr(interface, "verbose", verbose)
        self.log_stream = log_stream or LogStream(
            name=f"{self.name}LogStream", 
            group=interface.log_group if interface else None,
            verbose=self.verbose,
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
        