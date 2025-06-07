# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional, List

from x17_intelligence.handler.base import BaseHandler
from x17_intelligence.model.base import BaseModel

from x17_base.particle.log import LogStream
from x17_base.particle.log import LogGroup

class BaseInterface():
    """
    Abstract base interface for all LLM wrappers.
    Provides the minimal API for stateless inference.
    
    """
    def __init__(
        self, 
        name: str,
        log_group: Optional[LogGroup] = None,
        handler: Optional[BaseHandler] = None,
        verbose: bool = True,
    ):
        self.name = name or f"{self.__class__.__name__}"
        self.verbose = verbose
        self.models = {}
        self.log_group = log_group or LogGroup(
            name=f"{self.name}LogGroup",
        )
        self.log_stream = LogStream(
            name=f"{self.name}LogStream", 
            group=self.log_group,
        )
        if self.log_stream not in self.log_group.streams:
            self.log_group.register_stream(self.log_stream)
            
        self.handler = handler or BaseHandler(
            interface=self, 
            name=f"{self.name}Handler",
        )
        self.log_group.register_stream(self.handler.log_stream)

    def set_handler(self, handler: BaseHandler) -> None:
        """
        Set the handler for the interface.
        """
        self.handler = handler
        self.log_group.register_stream(handler.log_stream)
    
    def add_model(
        self, 
        model: BaseModel,
    ) -> None:
        """
        Add a model to the interface.
        """
        model.interface = self
        if hasattr(model, "log_stream") and model.log_stream and self.log_group:
            self.log_group.register_stream(model.log_stream)
        
        self.models[model.name] = model
        self.log_stream.register_stream(model.log_stream)
        self.log(
            message=f"Model {model.name} added to interface {self.name}",
            context="add_model",
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
        
        