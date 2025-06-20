from abc import ABC
from typing import Any, Dict, Optional, Union

import docker
from docker.client import DockerClient
from x17_base.particle.log.log_group import LogGroup
from x17_base.particle.log.log_stream import LogStream

class MountBase(ABC):
    
    def __init__(
        self,
        docker_client: Optional[DockerClient] = None,
        name: Optional[str] = None,
        mode: Optional[str] = None,
        chmod: Optional[bool] = False,
        permission: Optional[Dict[str, Union[int, str]]] = None,
        verbose: Optional[bool] = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
    ):
        self.docker_client = docker_client or docker.from_env()
        self.verbose = verbose
        self.log_stream = log_stream or LogStream(
            group=log_group,
            name=name,
            verbose=self.verbose,
        )
        self.name = name
        self.mode = mode or "rw"
        self.chmod = chmod or False
        self.permission = permission or {}

    def reload(self, **kwargs) -> None:
        pass

    def refresh(self, **kwargs) -> None:
        pass
    
    def exists(self, **kwargs) -> bool:
        return False

    def create(self, **kwargs) -> None:
        pass

    def delete(self, **kwargs) -> None:
        pass