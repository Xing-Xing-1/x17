from typing import Optional, Dict, Any

import docker
from docker.client import DockerClient
from x17_base.particle.text.id import Id
from x17_base.particle.log.log_group import LogGroup
from x17_base.particle.log.log_stream import LogStream

from x17_container.dockers.base.configuration import Configuration
from x17_container.dockers.base.attributes import Attributes

class Resource:
    """
    Represents a Docker resource, such as a network or volume.
    This class provides basic functionality for managing Docker resources
    and integrates with logging capabilities.

    Attributes:
        docker_client (DockerClient): the native docker client instance.
        name (str): name of the resource will be class name if not specified.
        verbose (bool): flag to enable verbose logging output.
        log_stream (LogStream): resource level log stream for logging messages.
        log_group (LogGroup): component level log group for organizing logs.

    """

    def __init__(
        self,
        docker_client: DockerClient = None,
        configuration: Optional[Configuration | Dict[str, Any]] = None,
        attributes: Optional[Attributes | Dict[str, Any]] = None,
        verbose: bool = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
    ):
        self.docker_client = docker_client or docker.from_env()
        self.physical_id = Id.uuid(length=4)
        if isinstance(configuration, Configuration):
            self.configuration = configuration
        else:
            self.configuration = Configuration.from_dict(configuration or {})
        if isinstance(attributes, Attributes):
            self.attributes = attributes
        else:
            self.attributes = Attributes.from_dict(attributes or {})
        
        self.log_stream = log_stream or LogStream(
            name=self.name,
            verbose=verbose,
            group=log_group,
        )

    @property
    def type(self) -> str:
        return self.__class__.__name__
    
    @property
    def name(self) -> str:
        return (
            getattr(self.configuration, "name", None) or
            getattr(self.attributes, "name", None) or
            f"{self.__class__.__name__}-{self.physical_id}"
        )

    def __str__(self):
        return self.name or ""

    def __repr__(self):
        return f"{self.type}(name={self.name})"

    def describe(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "configuration": self.configuration.to_dict(),
            "attributes": self.attributes.to_dict(),
        }
        
    def create(self) -> "Resource":
        pass
    
    def remove(self) -> None:
        pass
    
    def load(self) -> "Resource":
        pass
    
    def exists(self) -> bool:
        pass
    