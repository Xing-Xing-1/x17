import hashlib
from pathlib import Path
from typing import Any, Dict, Optional, Union

import docker
from docker.client import DockerClient
from docker.models.volumes import Volume as DockerVolume
from x17_base.particle.log.log_group import LogGroup
from x17_base.particle.log.log_stream import LogStream
from x17_base.particle.storage.storage import Storage

from x17_container.dockers.mount.base import MountBase


class MountTmpfs(MountBase):
    MODE_TO_OCTAL = {
        "rw": "0755",
        "ro": "0555",
        "r": "0444",
        "w": "0222",
        "x": "0111",
        "none": "0000",
    }

    def __init__(
        self,
        target: Union[str, Path],
        docker_client: Optional[DockerClient] = None,
        size: Optional[int | Storage] = None,
        mode: Optional[str] = None,
        name: Optional[str] = None,
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
        if isinstance(size, Storage):
            self.size = int(size.base)
        elif isinstance(size, int):
            self.size = size
        else:
            self.size = int(Storage(64, "mb").base)
        self.target = Path(target)
        if self.mode == "ro":
            self.log_stream.warn(
                "Docker tmpfs does not support true read-only behavior; "
            )
        
        
    @property
    def key(self) -> str:
        return hashlib.sha256(
            f"{self.name}:{self.target}".encode("utf-8")
        ).hexdigest()
        
    @property
    def octal_mode(self) -> str:
        return self.MODE_TO_OCTAL.get(self.mode, "0000")

    @property
    def chmod_script(self) -> Optional[str]:
        return None

    @property
    def permission_script(self) -> Optional[str]:
        return None
    
    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "target": str(self.target),
            "size": self.size,
            "mode": self.mode,
            "octal_mode": self.octal_mode,
            "name": self.name,
            "chmod": self.chmod,
            "permission": self.permission,
            "key": self.key,
        }
        
    def __str__(self) -> str:
        return self.name or ""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self.name}, target={self.target})"
        )
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MountTmpfs):
            return False
        return (
            self.name == other.name
            and self.target == other.target
            and self.size == other.size
            and self.mode == other.mode
        )
    
    def __ne__(self, value):
        return not self.__eq__(value)
    
    def get_docker_volume(self) -> DockerVolume:
        return None
    
    def to_docker_host(self) -> None:
        return None

    def to_docker_volume(self) -> None:
        return None
    
    def to_docker_tmpfs(self) -> Dict[str, str]:
        opts = []
        if self.size:
            opts.append(f"size={self.size}m")
        if self.permission:
            uid = self.permission.get("uid")
            gid = self.permission.get("gid")
            if uid is not None:
                opts.append(f"uid={uid}")
            if gid is not None:
                opts.append(f"gid={gid}")
        if self.mode:
            try:
                opts.append(f"mode={self.octal_mode}")
            except Exception:
                self.log_stream.warning(f"Invalid mode for tmpfs: {self.mode}")
        return {
            str(self.target): ",".join(opts)
        }
    
    def exists(self):
        return True
    
    def to_docker_mount(self) -> Dict[str, str]:
        return self.to_docker_tmpfs()
