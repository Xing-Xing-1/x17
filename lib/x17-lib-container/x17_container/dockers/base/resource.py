from typing import Optional

import docker
from docker.client import DockerClient
from x17_base.particle.log.log_group import LogGroup
from x17_base.particle.log.log_stream import LogStream


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
        verbose: bool = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
        name: Optional[str] = None,
    ):
        self.docker_client = docker_client or docker.from_env()
        self.verbose = verbose
        self.log_stream = log_stream or LogStream(
            group=log_group,
            name=name or self.__class__.__name__,
            verbose=self.verbose,
        )
        self.name = name

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def __str__(self):
        return self.name or ""

    def __repr__(self):
        return f"{self.type}(name={self.name})"
