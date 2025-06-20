import hashlib
from pathlib import Path
from typing import Any, Dict, Optional, Union

import docker
from docker.client import DockerClient
from docker.models.volumes import Volume as DockerVolume
from x17_base.particle.log.log_group import LogGroup
from x17_base.particle.log.log_stream import LogStream

from x17_container.dockers.mount.base import MountBase


class MountVolume(MountBase):

    @classmethod
    def from_docker(
        cls,
        docker_volume: DockerVolume,
        docker_client: Optional[DockerClient] = None,
        mode: Optional[str] = None,
        chmod: Optional[bool] = None,
        permission: Optional[Dict[str, Union[int, str]]] = None,
        verbose: Optional[bool] = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
    ) -> "MountVolume":
        return cls(
            docker_client=docker_client,
            docker_volume=docker_volume,
            name=docker_volume.name,
            mode=mode,
            chmod=chmod,
            permission=permission,
            verbose=verbose,
            log_stream=log_stream,
            log_group=log_group,
        )

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        docker_client: Optional[DockerClient] = None,
        verbose: Optional[bool] = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
    ) -> "MountVolume":
        return cls(
            docker_client=docker_client,
            id=data.get("id"),
            short_id=data.get("short_id"),
            name=data.get("name"),
            mountpoint=data.get("mountpoint"),
            driver=data.get("driver"),
            driver_opts=data.get("driver_opts"),
            labels=data.get("labels"),
            scope=data.get("scope"),
            mode=data.get("mode"),
            chmod=data.get("chmod"),
            permission=data.get("permission"),
            verbose=verbose,
            log_stream=log_stream,
            log_group=log_group,
        )

    def __init__(
        self,
        docker_client: Optional[DockerClient] = None,
        docker_volume: Optional[DockerVolume] = None,
        id: Optional[str] = None,
        short_id: Optional[str] = None,
        name: Optional[str] = None,
        mountpoint: Optional[str] = None, # Mount point in the host
        driver: Optional[str] = None,
        driver_opts: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
        scope: Optional[str] = None,
        mode: Optional[str] = None,
        chmod: Optional[bool] = None,
        permission: Optional[Dict[str, Union[int, str]]] = None,
        verbose: Optional[bool] = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
    ):
        super().__init__(
            docker_client=docker_client,
            name=name,
            mode=mode,
            chmod=chmod,
            permission=permission,
            verbose=verbose,
            log_stream=log_stream,
            log_group=log_group,
        )
        if docker_volume:
            self.docker_volume = docker_volume
            self.name = docker_volume.name
        elif name:
            self.name = name
            self.docker_volume = self.get_docker_volume()
        else:
            self.name = name
            self.docker_volume = None

        if self.docker_volume:
            self.load()
        else:
            self.id = id
            self.short_id = short_id
            self.mountpoint = mountpoint
            self.path = Path(self.mountpoint) if self.mountpoint else None
            self.driver = driver
            self.driver_opts = driver_opts or {}
            self.labels = labels or {}
            self.scope = scope
            self.created_at = None

    @property
    def key(self) -> str:
        return hashlib.sha256(f"{self.name}:{self.path}".encode("utf-8")).hexdigest()

    @property
    def chmod_script(self) -> Optional[str]:
        if self.permission:
            return None
        if self.chmod and self.mountpoint:
            return f"chmod -R 777 {self.mountpoint}"
        return None

    @property
    def permission_script(self) -> Optional[str]:
        if not self.mountpoint or not self.permission:
            return None
        cmds = []
        uid = self.permission.get("uid")
        gid = self.permission.get("gid")
        mode = self.permission.get("mode")
        if uid is not None and gid is not None:
            cmds.append(f"chown -R {uid}:{gid} {self.path}")
        if mode is not None:
            cmds.append(f"chmod -R {oct(mode)[2:]} {self.path}")
        return " && ".join(cmds) if cmds else None

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "id": self.id,
            "short_id": self.short_id,
            "mountpoint": self.mountpoint,
            "path": str(self.path) if self.path else None,
            "created_at": self.created_at,
            "driver": self.driver,
            "driver_opts": self.driver_opts,
            "labels": self.labels,
            "scope": self.scope,
            "mode": self.mode,
            "chmod": self.chmod,
            "permission": self.permission,
            "key": self.key,
        }

    def __str__(self) -> str:
        return self.name or ""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self.name}, mountpoint={self.mountpoint})"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MountVolume):
            return False
        return self.name == other.name and self.mountpoint == other.mountpoint

    def __ne__(self, value):
        return not self.__eq__(value)

    def get_docker_volume(self) -> DockerVolume:
        if self.name:
            try:
                self.docker_volume = self.docker_client.volumes.get(self.name)
            except Exception as e:
                self.docker_volume = None
        else:
            self.docker_volume = None
        return self.docker_volume

    def refresh(self) -> None:
        if not self.docker_volume:
            self.get_docker_volume()
        else:
            self.docker_volume.reload()

    def load(self) -> None:
        if self.docker_volume:
            self.id = self.docker_volume.id
            self.short_id = self.docker_volume.short_id
            self.name = self.docker_volume.name
            self.created_at = self.docker_volume.attrs.get("CreatedAt", None)
            self.driver = self.docker_volume.attrs.get("Driver", "local")
            self.mountpoint = self.docker_volume.attrs.get("Mountpoint", None)
            self.path = Path(self.mountpoint) if self.mountpoint else None
            self.labels = self.docker_volume.attrs.get("Labels", {})
            self.driver_opts = self.docker_volume.attrs.get("Options", {})
            self.scope = self.docker_volume.attrs.get("Scope", None)

    def reload(self) -> None:
        self.refresh()
        self.load()

    def to_docker_host(self) -> Dict[str, Dict[str, str]]:
        return None

    def to_docker_volume(self) -> Dict[str, Dict[str, str]]:
        return {
            self.name: {
                "bind": self.mountpoint,
                "mode": self.mode,
            }
        }

    def to_docker_tmpfs(self) -> Optional[Dict]:
        return None
    
    def to_docker_mount(self) -> Dict[str, Dict[str, str]]:
        return self.to_docker_volume()

    def exists(self) -> bool:
        try:
            self.docker_client.volumes.get(
                self.name,
            )
            return True
        except docker.errors.NotFound:
            return False

    def create(
        self,
        force: Optional[bool] = False,
        check: Optional[bool] = True,
    ) -> None:
        if self.exists():
            self.log_stream.info(f"Volume {self.name} already exists.")
            if force:
                self.delete()
            else:
                self.reload()

        if not self.exists():
            self.log_stream.info(f"Creating volume {self.name}.")
            try:
                self.docker_volume = self.docker_client.volumes.create(
                    name=self.name,
                    driver=self.driver,
                    driver_opts=self.driver_opts,
                    labels=self.labels,
                )
                self.reload()
            except Exception as e:
                message = f"Failed to create volume {self.name}: {e}"
                if check:
                    raise RuntimeError(message) from e
                else:
                    self.log_stream.error(message)

    def delete(
        self,
        force: Optional[bool] = True,
        check: Optional[bool] = True,
    ) -> None:
        if self.exists():
            self.log_stream.info(f"Deleting volume {self.name}.")
            try:
                self.docker_volume.remove(force=force)
            except Exception as e:
                message = f"Failed to delete volume {self.name}: {e}"
                if check:
                    raise RuntimeError(message) from e
                else:
                    self.log_stream.error(message)
        else:
            message = f"Volume {self.name} does not exist, nothing to delete."
            if check:
                raise RuntimeError(message)
            else:
                self.log_stream.error(message)
