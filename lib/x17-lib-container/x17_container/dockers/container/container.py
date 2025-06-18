from typing import Optional, Dict, List, Any
from docker.models.containers import Container as DockerContainer
from docker.client import DockerClient as DockerClient
import docker
import threading

from x17_base.particle.log.log_stream import LogStream
from x17_base.particle.log.log_group import LogGroup

from x17_container.dockers.image.image import Image


class Container:

    @classmethod
    def from_docker(
        cls,
        docker_container: DockerContainer,  # Docker container instance
        docker_client: Optional[DockerClient] = None,  # Docker client instance
    ):
        if not isinstance(docker_container, DockerContainer):
            raise TypeError("Expected a DockerContainer instance.")

        if not isinstance(docker_client, DockerClient):
            raise ValueError("Docker container cannot be None or empty.")

        return cls(
            docker_client=docker_client or docker.from_env(),
            docker_container=docker_container,
        )

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        docker_client: Optional[DockerClient] = None,  # Docker client instance
    ) -> "Container":
        args = {
            "docker_client": docker_client or docker.from_env(),
            "image": data.get("image"),
            "image_obj": data.get("image_obj"),  # Optional Image object as dict
            "name": data.get("name"),
            "ports": data.get("ports"),
            "volumes": data.get("volumes"),
            "environment": data.get("environment"),
            "command": data.get("command"),
            "network": data.get("network"),
            "auto_remove": data.get("auto_remove", False),
            "detach": data.get("detach", True),
        }
        extra = {k: v for k, v in data.items() if k not in args}
        return cls(**args, **extra)

    def __init__(
        self,
        image: Optional[str | Image] = None,
        docker_client: Optional[DockerClient] = None,
        docker_container: Optional[DockerContainer] = None,
        name: Optional[str] = None,
        ports: Optional[Dict[str, Any]] = None,
        volumes: Optional[List[Dict[str, Any]]] = None,
        environment: Optional[List[str]] = None,
        command: Optional[List[str]] = None,
        network: Optional[str] = None,
        auto_remove: bool = False,
        detach: bool = True,
        # x17 base specific parameters
        verbose: bool = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
        log_encoding: Optional[str] = "utf-8",
        log_errors: Optional[str] = "ignore",
        # additional parameters
        **kwargs: Any,
    ):
        # Echo system variables
        self.verbose = verbose
        self.log_encoding = log_encoding
        self.log_errors = log_errors
        if log_stream:
            self.log_stream = log_stream
        else:
            self.log_stream = LogStream(
                group=log_group,
                name=name,
                verbose=self.verbose,
            )
        
        # Initialize Docker client and container
        self.docker_client = docker_client or docker.from_env()
        
        # prepare image 
        if isinstance(image, Image):
            self.image = image
            self.image.__setattr__("docker_client", self.docker_client)
            self.image.__setattr__("log_stream", self.log_stream)
            self.image.__setattr__("log_group", self.log_group)
        elif isinstance(image, str):
            self.image = Image(
                docker_client = docker_client,
                name=image,
                log_stream=self.log_stream,
                log_encoding=self.log_encoding,
                log_errors=self.log_errors,
            )
        else:
            raise TypeError("Image must be a string or an instance of Image class.")

        if docker_container:
            self.docker_container = docker_container
        else:
            self.build(
                name=name,
                ports=ports,
                volumes=volumes,
                environment=environment,
                command=command,
                network=network,
                auto_remove=auto_remove,
                detach=detach,
                **kwargs,
            )
        self.detach = detach
        self.auto_remove = auto_remove
        self.load_attrs()
        
        # additional attributes from kwargs goes here
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "image": self.image,
            "name": self.name,
            "ports": self.ports,
            "volumes": self.volumes,
            "environment": self.environment,
            "command": self.command,
            "network": self.network,
            "detach": self.detach,
            "auto_remove": self.auto_remove,
        }

    @property
    def status(self) -> str:
        self.refresh()
        return self.docker_container.status
    
    @property
    def ports(self) -> Dict[str, Any]:
        self.refresh()
        return self.docker_container.attrs.get("NetworkSettings", {}).get("Ports", {})

    @property
    def is_running(self) -> bool:
        self.refresh()
        return self.docker_container.status == "running"
    
    @property
    def is_stopped(self) -> bool:
        self.refresh()
        return self.docker_container.status == "exited"
    
    def __str__(self):
        return self.id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, image={self.image}, name={self.name}, status={self.status})"

    def build(
        self,
        name: Optional[str] = None,
        ports: Optional[Dict[str, Any]] = None,
        volumes: Optional[List[Dict[str, Any]]] = None,
        environment: Optional[List[str]] = None,
        command: Optional[List[str]] = None,
        network: Optional[str] = None,
        auto_remove: bool = False,
        detach: bool = True,
        **kwargs: Any,
    ) -> "Container":
        self.docker_container = self.docker_client.containers.create(
            image=self.image.name,
            name=name,
            ports=ports,
            volumes=volumes,
            environment=environment,
            command=command,
            network=network,
            detach=detach,
            auto_remove=auto_remove,
        )
        self.refresh()
        self.log_stream.log(f"Container created with image {self.image.name}.")

    def load_attrs(self):
        self.id = self.docker_container.id
        self.name = self.docker_container.name
        self.volumes = self.docker_container.attrs.get("Mounts", {})
        self.environment = self.docker_container.attrs.get("Config", {}).get("Env", [])
        self.command = self.docker_container.attrs.get("Config", {}).get("Cmd", [])
        self.network = list(
            self.docker_container.attrs.get("NetworkSettings", {})
            .get("Networks", {})
            .keys()
        )

    def refresh(self):
        try:
            self.docker_container.reload()
            self.load_attrs()
        except Exception as e:
            raise RuntimeError(f"Failed to reload container {self.name}: {e}")
        return self

    def start(self, **kwargs) -> "Container":
        if self.docker_container.status == "running":
            self.log_stream.log(f"Container {self.name} already running.")
            self.refresh()
            return self
        else:
            try:
                self.docker_container.start(**kwargs)
                self.log_stream.log(f"Container {self.name} started successfully.")
                return self
            except Exception as e:
                self.log_stream.log(f"Error: {e}", level="ERROR")
                raise RuntimeError(f"Failed to start container {self.name}: {e}")

    def remove(self, force: bool = False, **kwargs):
        try:
            self.docker_container.remove(force=force, **kwargs)
            self.docker_container = None
            self.log_stream.log(f"Container {self.name} removed successfully.")
        except Exception as e:
            self.log_stream.log(f"Error: {e}", level="ERROR")
            raise RuntimeError(f"Failed to remove container {self.name}: {e}")

    def stop(self, **kwargs) -> "Container":
        try:
            self.docker_container.stop(**kwargs)
            self.refresh()
            self.log_stream.log(f"Container {self.name} stopped successfully.")
            return self
        except Exception as e:
            self.log_stream.log(f"Error: {e}", level="ERROR")
            raise RuntimeError(f"Failed to stop container {self.name}: {e}")

    def wait(self, timeout: Optional[int] = None):
        try:
            return self.docker_container.wait(timeout=timeout)
        except Exception as e:
            raise RuntimeError(f"Failed to wait for container {self.name}: {e}")

    def parse_log_line(self, line: str):
        return line.decode(self.log_encoding, errors=self.log_errors).strip()

    def parse_log_lines(self, lines: List[str]) -> List[str]:
        return [self.parse_log_line(line) for line in lines]

    def batch_logs(
        self,
        stdout: bool = True,
        stderr: bool = True,
        **kwargs,
    ) -> List[str]:
        try:
            logs = self.docker_container.logs(
                stdout=stdout,
                stderr=stderr,
                stream=False,
                **kwargs,
            )
            return self.parse_log_lines(logs.splitlines())
        except Exception as e:
            self.log_stream.log(f"Error: {e}", level="ERROR")
            return []

    def stream_logs(
        self,
        stdout: bool = True,
        stderr: bool = True,
        **kwargs,
    ):
        try:
            logs = self.docker_container.logs(
                stream=True,
                stdout=stdout,
                stderr=stderr,
                follow=True,
                **kwargs,
            )
            for line in logs:
                self.log_stream.log(
                    self.parse_log_line(line),
                )
        except Exception as e:
            self.log_stream.log(f"Error: {e}", level="ERROR")

    def log(
        self,
        stdout=True,
        stderr=True,
        stream=True,
        **kwargs,
    ) -> threading.Thread:
        if stream:
            thread = threading.Thread(target=self.stream_logs, daemon=True)
            thread.start()
            return thread
        else:
            logs = self.batch_logs(stdout=stdout, stderr=stderr, **kwargs)
            for log in logs:
                self.log_stream.log(log)
            return logs

    def export(self) -> Dict[str, Any]:
        self.refresh()
        result = self.dict
        result.update(
            {
                k: v
                for k, v in self.__dict__.items()
                if k not in result and not k.startswith("_")
            }
        )
        return result
