#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, Dict, Union, Any, List
from pangu.particle.log.log_stream import LogStream
from pangu.particle.log.log_group import LogGroup


class AwsClient:
    """
    Base class for AWS clients.
    This class provides a common interface for AWS clients, including logging and plugin registration.
    Normally set the log module to log group.
    
    Attributes:
        account_id (str): The AWS account ID.
        region (str): The AWS region.
        service (str): The AWS service name.
        plugin (Dict[str, Any]): A dictionary of plugins.
        log_stream (LogStream): The log stream for logging.
        max_paginate (int): The maximum number of items to paginate through.

    """

    REGION_NAME = "ap-southeast-2"
    MAX_PAGINATE = 100

    def __init__(
        self,
        account_id: Optional[str] = None,
        service: Optional[str] = None,
        region: Optional[str] = None,
        plugin: Optional[Dict[str, Any]] = None,
        log_group: Optional[LogGroup] = None,
        max_paginate: Optional[int] = None,
        **kwargs: Optional[Dict[str, Any]],
    ):
        self.account_id = account_id
        self.region = region or self.REGION_NAME
        self.service = service
        self.plugin = plugin or {}
        self.extra_config = kwargs
        self.max_paginate = max_paginate or self.MAX_PAGINATE
        self.log_stream = LogStream(
            name=f"{self.__class__.__name__}:{self.service}:{self.region}:{self.account_id}",
        )
        if log_group:
            self.log_group = log_group
            self.log_stream = self.log_group.register_stream(self.log_stream)
        else:
            self.log_group = None

    def register_plugin(self, name: str, plugin: Any):
        """
        Register a plugin to the client.
        Args:
            name (str): The name of the plugin.
            plugin (Any): The plugin to register.
        Returns:
            Tuple[str, Any]: The name and plugin.
        """
        if name in self.plugin:
            raise ValueError(f"Plugin {name} already registered.")
        self.plugin[name] = plugin
        return name, plugin

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(service={self.service}, region={self.region}, account_id={self.account_id})"

    @property
    def dict(self):
        return {
            "account_id": self.account_id,
            "region": self.region,
            "service": self.service,
            "plugin": self.plugin,
            "log_stream": self.log_stream.name,
        }

    def log(
        self,
        message: str,
        level: str = "INFO",
        **kwargs: Optional[Dict[str, str]],
    ):
        """
        Log a message to the log stream.
        Args:
            message (str): The message to log.
            level (str): The log level (e.g., INFO, DEBUG, ERROR).
            **kwargs: Additional keyword arguments for logging.

        """
        self.log_stream.log(
            level=level,
            message=message,
            **kwargs,
        )

    def pop_list(
        self,
        data: List,
        index: int = 0,
        default: Optional[Any] = None,
    ) -> Union[Dict[str, Any], None]:
        """
        Pop out a list of data by index.
        Args:
            data (List): The list to pop.
            index (int): The index to pop.
            default (Any, optional): The default value if the index is out of range.
        Returns:
            Union[Dict[str, Any], None]: The popped value or default.

        """
        if index < 0 or index >= len(data):
            return default

        try:
            return data.pop(index)
        except Exception as e:
            return default

    def slice_list(
        self,
        data: List,
        start: int = 0,
        end: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Return a slice of the list between start and end indexes.
        Args:
            data (List): The list to slice.
            start (int): The starting index.
            end (int, optional): The ending index (inclusive-exclusive). Defaults to end of list.
        Returns:
            List[Any]: The sliced sublist.

        """
        if end is None:
            end = len(data)
        return data[start:end]

    def strip_params(
        self,
        **kwargs: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Strip None values from a group of kwargs.
        And return a dictionary of the remaining values.
        Args:
            **kwargs: The keyword arguments to strip.
        Returns:
            Dict: A dictionary of the remaining values.

        """
        return {k: v for k, v in kwargs.items() if v is not None}
