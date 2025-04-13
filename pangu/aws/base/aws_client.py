#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, Dict, Union, Any
from pangu.particle.log.log_stream import LogStream
from pangu.particle.log.log_group import LogGroup


class AwsClient: 
    REGION_NAME = "ap-southeast-2"
    MAX_PAGINATE = 100
    
    @classmethod
    def get_region(cls) -> str:
        return cls.REGION_NAME
    
    @classmethod
    def get_max_paginate(cls) -> int:
        return cls.MAX_PAGINATE
    
    @classmethod
    def set_default(cls, region = None, max_paginate = None):
        if region:
            cls.REGION_NAME = region
        if max_paginate:
            cls.MAX_RECURSION = max_paginate
    
    
    def __init__(
        self,
        account_id: Optional[str] = None,
        service: Optional[str] = None,
        region: Optional[str] = None,
        plugin: Optional[Dict[str, Any]] = None,
        log_group: Optional[LogGroup] = None,
        **kwargs: Optional[Dict[str, Any]],
    ):
        """
        Initialize the AwsClient instance.

        """
        self.account_id = account_id
        self.region = region or self.REGION_NAME
        self.service = service
        self.plugin = plugin or {}
        self.extra_config = kwargs
        self.class_name = self.__class__.__name__.lower()
        self.log_stream = LogStream(
            name=f"{self.class_name}:{self.service}:{self.region}:{self.account_id}",
        )
        if log_group:
            self.log_group = log_group
            self.log_stream = self.log_group.register_stream(self.log_stream)
        else:
            self.log_group = None
            
        
    def register_plugin(self, name: str, plugin: Any):
        if name in self.plugin:
            raise ValueError(f"Plugin {name} already registered.")
        self.plugin[name] = plugin
        return name, plugin
        
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return f"{self.__class__.__name__}(service={self.service}, region={self.region}, account_id={self.account_id})"

    def __dict__(self):
        return {
            "account_id": self.account_id,
            "region": self.region,
            "service": self.service,
            "plugin": self.plugin,
            "log_stream": self.log_stream.name,
        }

    def log(self, level: str, message: str):
        self.log_stream.log(level, message)