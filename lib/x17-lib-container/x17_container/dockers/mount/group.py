from typing import List, Optional, Dict, Union, Any
from docker.client import DockerClient
import docker
from pathlib import Path

from x17_container.dockers.mount.host import MountHost
from x17_container.dockers.mount.tmpfs import MountTmpfs
from x17_container.dockers.mount.volume import MountVolume
from x17_base.particle.log.log_stream import LogStream
from x17_base.particle.log.log_group import LogGroup



class MountGroup:
    def __init__(
        self,
        docker_client: DockerClient = None,
        name: Optional[str] = None,
        volumes: Optional[List[MountVolume]] = None,
        hosts: List[MountHost] = None,
        tmpfses: List[MountTmpfs] = None,
        retain_on_delete: Optional[bool] = True,
        verbose: Optional[bool] = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
    ):
        self.docker_client = docker_client or docker.from_env()
        self.name = name
        self.volumes = volumes if volumes else []
        self.hosts = hosts if hosts else []
        self.tmpfses = tmpfses if tmpfses else []
        self.retain_on_delete = retain_on_delete
        self.verbose = verbose
        self.log_stream = log_stream or LogStream(
            group=log_group,
            name=name,
            verbose=self.verbose,
        )
    
    @property
    def all_mounts(self) -> List[Union[MountHost, MountTmpfs, MountVolume]]:
        return self.hosts + self.tmpfses + self.volumes
    
    @property
    def num_volumes(self) -> int:
        return len(self.volumes)
    
    @property
    def num_hosts(self) -> int: 
        return len(self.hosts)
    
    @property
    def num_tmpfses(self) -> int:
        return len(self.tmpfses)
    
    @property
    def num_mounts(self) -> int:
        return len(self.all_mounts)
    
    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "num_mounts": self.num_mounts,
            "num_volumes": self.num_volumes,
            "num_hosts": self.num_hosts,
            "num_tmpfses": self.num_tmpfses,
            "volumes": [v.dict for v in self.volumes],
            "hosts": [h.dict for h in self.hosts],
            "tmpfses": [t.dict for t in self.tmpfses],
            "retain_on_delete": self.retain_on_delete,
        }
    
    def __str__(self):
        return self.name or ""
    
    def __repr__(self):
        return f"MountGroup(name={self.name}, num_mounts={self.num_mounts})"
    
    def add_mount(
        self, 
        mount: Union[MountHost, MountTmpfs, MountVolume],
    ):
        if isinstance(mount, MountHost):
            self.hosts.append(mount)
        elif isinstance(mount, MountTmpfs):
            self.tmpfses.append(mount)
        elif isinstance(mount, MountVolume):
            self.volumes.append(mount)
        else:
            raise TypeError("Mount must be an instance of MountHost, MountTmpfs, or MountVolume")

    def get_mount_by_name(
        self,
        name: str,
    ) -> Optional[Union[MountHost, MountTmpfs, MountVolume]]:
        for mount in self.all_mounts:
            if mount.name == name:
                return mount
        return None
    
    def get_mount_by_target(
        self,
        target: Union[str, Path],
    ) -> Optional[Union[MountHost, MountTmpfs, MountVolume]]:
        for mount in self.all_mounts:
            if not hasattr(mount, 'target'):
                continue
            else:
                if Path(mount.target) == Path(target):
                    return mount
        return None
    
    def get_mount_by_mountpoint(
        self,
        mountpoint: Union[str, Path],
    ) -> Optional[Union[MountHost, MountTmpfs, MountVolume]]:
        for mount in self.all_mounts:
            if not hasattr(mount, 'mountpoint'):
                continue
            else:
                if Path(mount.mountpoint) == Path(mountpoint):
                    return mount
        return None

    def delete_mount(
        self,
        mount: Union[MountHost, MountTmpfs, MountVolume],
    ) -> bool:
        if mount in self.hosts:
            self.hosts.remove(mount)
        elif mount in self.tmpfses:
            self.tmpfses.remove(mount)
        elif mount in self.volumes:
            self.volumes.remove(mount)
        else:
            return False
        mount.delete()
        self.log_stream.info(f"Mount {mount.name} deleted")
        return True

    def unlink_mount(
        self,
        mount: Union[MountHost, MountTmpfs, MountVolume],
    ) -> bool:
        if mount in self.hosts:
            self.hosts.remove(mount)
        elif mount in self.tmpfses:
            self.tmpfses.remove(mount)
        elif mount in self.volumes:
            self.volumes.remove(mount)
        else:
            return False
        self.log_stream.info(f"Mount {mount.name} unlinked")
        return True
    
    def reload(
        self,
    ) -> None:
        for mount in self.all_mounts:
            try:
                mount.reload()
            except Exception as e:
                self.log_stream.error(f"Failed to reload mount {mount}: {e}")
        self.log_stream.info("Mounts reloaded")

    def refresh(
        self,
    ) -> None:
        for mount in self.all_mounts:
            mount.refresh()
        self.log_stream.info("Mounts refreshed")
        
    def exists(
        self,
    ) -> bool:
        return all(mount.exists() for mount in self.all_mounts)
        
    def to_docker_conf(
        self,
        use_mounts: Optional[bool] = False,
    ) -> Dict[str, Any]:
        tmpfs_conf: Dict[str, str] = {}
        volume_conf: Dict[str, Dict[str, str]] = {}
        for tmpfs in self.tmpfses:
            try:
                tmpfs_conf.update(tmpfs.to_docker_mount())
            except Exception as e:
                self.log_stream.warning(f"Failed to generate tmpfs config for {tmpfs}: {e}")

        for mount in self.hosts + self.volumes:
            try:
                volume_conf.update(mount.to_docker_mount())
            except Exception as e:
                self.log_stream.error(f"Failed to generate volume config for {mount}: {e}")

        if use_mounts:
            mounts = []
            for mount in self.all_mounts:
                if hasattr(mount, "to_docker_mount_obj"):
                    mounts.append(mount.to_docker_mount_obj())
            return {"mounts": mounts}
        else:
            return {"tmpfs": tmpfs_conf, "volumes": volume_conf}

    def create(
        self,
        force: Optional[bool] = False,
        check: Optional[bool] = True,
    ) -> None:
        for mount in self.all_mounts:
            mount.create(force=force, check=check)
        self.log_stream.info("Mounts created")
        return True
    
    def delete(
        self,
        force: Optional[bool] = True,
    ) -> None:
        if self.retain_on_delete:
            self.log_stream.info("Mounts retained on delete")
            return False
        else:
            for mount in self.all_mounts:
                mount.delete(force=force)
            self.log_stream.info("Mounts deleted")
            return True

