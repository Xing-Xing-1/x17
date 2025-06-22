import hashlib
import shutil
from pathlib import Path
from typing import Any, Dict, Optional, Union

import docker
from docker.client import DockerClient
from x17_base.particle.log.log_group import LogGroup
from x17_base.particle.log.log_stream import LogStream

from x17_container.dockers.mount.base import MountBase


class MountHost(MountBase):

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        docker_client: Optional[DockerClient] = None,
        verbose: Optional[bool] = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
    ) -> "MountHost":
        return cls(
            mountpoint=data.get("mountpoint"),
            target=data.get("target"),
            docker_client=docker_client,
            name=data.get("name"),
            mode=data.get("mode"),
            chmod=data.get("chmod"),
            permission=data.get("permission"),
            verbose=verbose,
            log_stream=log_stream,
            log_group=log_group,
        )

    def __init__(
        self,
        mountpoint: Union[str, Path],  # Host path
        target: Union[str, Path],  # Container path
        docker_client: Optional[DockerClient] = None,
        name: Optional[str] = None,
        mode: Optional[str] = None,
        chmod: Optional[bool] = False,
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
        self.mountpoint = Path(mountpoint)  # Host path
        self.target = Path(target)  # Container path
    
    @property
    def key(self) -> str:
        return hashlib.sha256(
            f"{self.mountpoint}:{self.target}".encode("utf-8")
        ).hexdigest()

    @property
    def chmod_script(self) -> Optional[str]:
        if self.permission:
            # If permission is provided, chmod is ignored
            return None
        if self.chmod and self.mountpoint.exists():
            return f"chmod -R 777 {self.mountpoint}"
        return None

    @property
    def permission_script(self) -> Optional[str]:
        if not self.mountpoint.exists() or not self.permission:
            return None
        cmds = []
        uid = self.permission.get("uid")
        gid = self.permission.get("gid")
        mode = self.permission.get("mode")
        if uid is not None and gid is not None:
            cmds.append(f"chown -R {uid}:{gid} {self.mountpoint}")
        if mode is not None:
            cmds.append(f"chmod -R {oct(mode)[2:]} {self.mountpoint}")
        return " && ".join(cmds) if cmds else None

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "mountpoint": str(self.mountpoint),
            "target": str(self.target),
            "mode": self.mode,
            "chmod": self.chmod,
            "permission": self.permission,
            "key": self.key,
        }

    def __str__(self) -> str:
        return f"{self.mountpoint} -> {self.target}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(mountpoint={self.mountpoint}, target={self.target})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MountHost):
            return False
        return (
            self.mountpoint == other.mountpoint
            and self.target == other.target
            and self.mode == other.mode
        )

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)
    
    def get_docker_volume(self) -> None:
        return None

    def to_docker_host(self) -> Dict[str, Dict[str, str]]:
        return {
            str(self.mountpoint): {
                "bind": str(self.target),
                "mode": self.mode,
            }
        }

    def to_docker_volume(self):
        return None

    def to_docker_tmpfs(self):
        return None
    
    def to_docker_mount(self) -> Dict[str, Dict[str, str]]:
        return self.to_docker_host()

    def exists(self) -> bool:
        return self.mountpoint.exists()

    def create(
        self,
        force: Optional[bool] = False,
        check: Optional[bool] = True,
    ) -> None:
        if self.exists():
            self.log_stream.info(f"Volume {self.name} already exists.")
            if force:
                self.delete()

        if not self.exists():
            self.log_stream.info(
                f"Creating binding from {self.mountpoint} to {self.target}."
            )
            try:
                self.mountpoint.mkdir(
                    parents=True,
                    exist_ok=force,
                )
            except Exception as e:
                message = f"Failed to create host mount {self.mountpoint}: {e}"
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
            self.log_stream.info(f"Deleting host {self.mountpoint}.")
            try:
                if force:
                    shutil.rmtree(
                        self.mountpoint, 
                        ignore_errors=True,
                    )
                else:
                    shutil.rmtree(
                        self.mountpoint,
                    )
            except Exception as e:
                message = f"Failed to delete host mount {self.mountpoint}: {e}"
                if check:
                    raise RuntimeError(message) from e
                else:
                    self.log_stream.error(message)
