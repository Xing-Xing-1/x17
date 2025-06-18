from __future__ import annotations 
from typing import Optional, Dict, List, Any
from typing import TYPE_CHECKING
from docker import DockerClient
import docker


if TYPE_CHECKING:
    from x17_container.dockers.container.container import Container


class Client:

    @classmethod
    def from_default(self) -> "Client":
        return Client(
            docker_client=docker.from_env(),
        )

    def __init__(
        self,
        docker_client: Optional[DockerClient] = None,
        base_url: Optional[str] = None,
        version: str = "auto",
        timeout: int = None,
        tls: Optional[bool] = None,
        user_agent: Optional[str] = None,
        credstore_env: Optional[Dict[str, str]] = None,
        use_ssh_client: bool = False,
        max_pool_size: int = 10,
    ):
        if docker_client and isinstance(docker_client, DockerClient):
            self.docker_client = docker_client
        else:
            self.docker_client = docker.DockerClient(
                base_url=base_url,
                version=version,
                timeout=timeout,
                tls=tls,
                user_agent=user_agent,
                credstore_env=credstore_env,
                use_ssh_client=use_ssh_client,
                max_pool_size=max_pool_size,
            )
        
        # If base_url is not provided, use the one from the Docker client
        self.base_url = base_url or self.docker_client.api.base_url
        self.version = version or self.docker_client.api.version()
        self.timeout = timeout or self.docker_client.api.timeout

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "base_url": self.base_url,
            "version": self.version,
            "timeout": self.timeout,
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        attributes = []
        for key, value in self.dict.items():
            if value:
                attributes.append(f"{key}={value}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def list_containers(
        self, 
        all: bool = True,
        filters: Optional[Dict[str, Any]] = None
    ) -> List["Container"]:
        result = []
        for container in self.docker_client.containers.list(
            all=all,
            filters=filters
        ):
            result.append(
                Container.from_docker(
                    container, 
                    self.docker_client,
                )
            )
        return result
        
    def get_container(
        self, 
        identity: str, # Container ID or name
    ) -> Optional[Container]:
        try:
            container = self.docker_client.containers.get(identity)
            return Container.from_docker(
                container, 
                self.docker_client,
            )
        except docker.errors.NotFound:
            return None
    
    def close(self):
        self.docker_client.close()


