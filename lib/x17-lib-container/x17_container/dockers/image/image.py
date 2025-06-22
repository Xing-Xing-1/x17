from typing import Optional, Dict, List, Any
from docker.client import DockerClient
from docker.models.images import Image as DockerImage
import docker
from pathlib import Path

from x17_base.particle.log.log_stream import LogStream
from x17_base.particle.log.log_group import LogGroup

from x17_container.dockers.image.imagebuild import ImageBuild
from x17_container.dockers.image.imageaction import ImageAction
from x17_container.dockers.image.imagetype import ImageType
from x17_container.dockers.image.imagemeta import ImageMeta

class Image:
    
    @classmethod
    def from_docker(
        cls,
        docker_image: DockerImage,
        docker_client: Optional[DockerClient] = None,
        buildparam: Optional[ImageBuild | Dict] = None,
        action: Optional[ImageAction] = None,
        skipsetup: bool = False,
        verbose: bool = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
    ) -> "Image":
        repotags = docker_image.attrs.get("RepoTags", [])
        if repotags:
            repository = repotags[0].split(":")[0]
            tag = repotags[0].split(":")[-1]
        else:
            repository = ""
            tag = "latest"
        return cls(
            docker_client=docker_client,
            docker_image=docker_image,
            repository=repository,
            tag=tag,
            buildparam=buildparam,
            action=action,
            skipsetup=skipsetup,
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
    ) -> "Image":
        return cls(
            docker_client=docker_client,
            repository=data.get("repository"),
            tag=data.get("tag"),
            buildparam=ImageBuild.from_dict(
                data.get("buildparam", {}),
            ),
            action=ImageAction.from_str(
                data.get("action", "MANUAL"),
            ),
            skipsetup=data.get("skipsetup", False),
            verbose=verbose,
            log_stream=log_stream,
            log_group=log_group,
        )
    
    def __init__(
        self,
        docker_client: DockerClient = None,
        docker_image: Optional[DockerImage] = None,
        repository: Optional[str] = None,
        tag: Optional[str] = None,
        buildparam: Optional[ImageBuild | Dict] = None,
        action: Optional[ImageAction] = None,
        skipsetup: bool = False,
        verbose: bool = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
    ):
        self.docker_client = docker_client or docker.from_env()
        self.repository = repository or ""
        self.tag = tag or "latest"
        self.verbose = verbose
        self.log_stream = log_stream or LogStream(
            group=log_group,
            name=self.name,
            verbose=self.verbose,
        )
        self.docker_image = docker_image
        self.action = action
        
        if not action:
            self.action = ImageAction("MANUAL")
        if isinstance(self.action, str):
            self.action = ImageAction.from_str(self.action)
            
        self.skipsetup = skipsetup
        self.buildparam = buildparam
        
        if isinstance(buildparam, dict):
            self.buildparam = ImageBuild(params=buildparam)
        else:
            self.buildparam = buildparam
        
        if self.buildparam and not self.buildparam.tag:
            self.buildparam.tag = f"{self.repository}:{self.tag or 'latest'}"
        
        self.load()
        if self.skipsetup:
            self.log_stream.info(f"Skipping setup for image {self.name}.")
        else:
            self.setup()
            
    @property
    def name(self) -> str:
        return f"{self.repository}:{self.tag}"
    
    @property
    def type(self) -> ImageType:
        if str(self.action) == "BUILD":
            return ImageType.BUILD
        elif str(self.action) == "PULL":
            return ImageType.PULL
        else:
            return ImageType.MANUAL
        
    @property
    def status(self) -> str:
        if self.exists():
            return "AVAILABLE"
        else:
            return "NOT_AVAILABLE"
    
    @property
    def full_status(self) -> str:
        return f"[{self.status}] {self.name or self.id} ({self.size})"
    
    @property
    def dockerlines(self) -> List[str]:
        lines = []
        if self.buildparam and self.buildparam.path:
            dockerfname = self.buildparam.dockerfile or "Dockerfile"
            dockerfpath = Path(self.buildparam.path) / dockerfname
            if dockerfpath.exists():
                with open(dockerfpath) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            lines.append(line)
        return lines
    
    @property
    def cascades(self) -> str:
        result = []
        if self.dockerlines and self.buildparam:
            for line in self.dockerlines:
                if line.strip().startswith("FROM "):
                    parts = line.strip().split()
                    if len(parts) > 1:
                        result.append(parts[1])
        return list(set(result))

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "repository": self.repository,
            "tag": self.tag,
            "type": str(self.type),
            "status": self.status,
            "full_status": self.full_status,
            "cascades": self.cascades,
            "buildparam": self.buildparam.dict if self.buildparam else None,
            "action": str(self.action) if self.action else None,
            "labels": self.labels,
            "tags": self.tags,
            "repotags": self.repotags,
            "repodigests": self.repodigests,
            "parent": self.parent,
            "comment": self.comment,
            "created": self.created,
            "docker_version": self.docker_version,
            "author": self.author,
            "config": self.config,
            "architecture": self.architecture,
            "variant": self.variant,
            "os": self.os,
            "size": self.size,
            "graph_driver": self.graph_driver,
            "rootfs": self.rootfs,
            "metadata": self.metadata,
            "descriptor": self.descriptor,
        }

    def __str__(self):
        return self.name or self.id or ""

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, id={self.id})"
    
    def load(self) -> None:
        if self.docker_image:
            self.id = self.docker_image.id
            self.labels = self.docker_image.labels
            self.tags = self.docker_image.tags
        else:
            self.id = None
            self.labels = {}
            self.tags = []
        
        if hasattr(self.docker_image, "attrs"):
            self.meta = ImageMeta(
                params=dict(self.docker_image.attrs),
            )
        else:
            self.meta = ImageMeta(params={})
        
        for key, value in self.meta.dict.items():
            if not hasattr(self, key):
                setattr(self, key, value)  
            
    def setup(self) -> "Image":
        if str(self.action) == "BUILD":
            self.build()
        elif str(self.action) == "PULL":
            self.pull()
        else:
            self.log_stream.info(f"No action for manual image {self.name}.")
         
    def exists(self) -> bool:
        try:
            self.docker_image = self.docker_client.images.get(self.name)
            return True
        except docker.errors.ImageNotFound:
            return False
            
    def pull(
        self,
        force: Optional[bool] = False,
        check: Optional[bool] = True,
    ) -> None:
        if self.exists():
            if force:
                self.log_stream.info(f"Force deleting image {self.name}.")
                self.delete()
            else:
                self.log_stream.info(f"Image {self.name} already exists.")
        else:
            try:
                self.log_stream.info(f"Pulling image {self.name}.")
                self.docker_image = self.docker_client.images.pull(
                    self.name,
                )
                self.load()
            except Exception as e:
                message = f"Failed to pull image {self.name}: {e}"
                if check:
                    raise RuntimeError(message) from e
                else:
                    self.log_stream.error(message)
            
    def build(
        self,
        force: Optional[bool] = False,
        check: Optional[bool] = True,
    ):
        if self.exists():
            if force:
                self.log_stream.info(f"Force deleting image {self.name}.")
                self.delete()
            else:
                self.log_stream.info(f"Image {self.name} already exists.")
        
        else:
            try:
                self.log_stream.info(f"Building image {self.name}.")
                self.docker_image, _ = self.docker_client.images.build(
                    **self.buildparam.dict
                )
                self.load()
                self.log_stream.info(f"Image {self.name} built successfully.")
            except Exception as e:
                message = f"Failed to build image {self.name}: {e}"
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
            try:
                self.docker_client.images.remove(
                    self.name,
                    force=force,
                )
                self.docker_image = None
                self.load()
                self.log_stream.info(f"Image {self.name} deleted successfully.")
            except Exception as e:
                message = f"Failed to delete image {self.name}: {e}"
                if check:
                    raise RuntimeError(message) from e
                else:
                    self.log_stream.error(message)
        else:
            message = f"Image {self.name} does not exist, nothing to delete."
            if check:
                raise RuntimeError(message)
            else:
                self.log_stream.error(message)          
        
        if self.cascades and force:
            for cascade in self.cascades:
                try:
                    self.docker_client.images.remove(cascade, force=force)
                    self.log_stream.info(f"Removed cascade image {cascade}.")
                except Exception as e:
                    message = f"Failed to remove cascade image {cascade}: {e}"
                    self.log_stream.error(message)
                         
    def export(self) -> Dict[str, Any]:
        return self.dict
    