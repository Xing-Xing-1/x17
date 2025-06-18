from typing import Optional, Dict, List, Any
from docker.client import DockerClient
from docker.models.images import Image as DockerImage
import docker

from x17_base.particle.log.log_stream import LogStream
from x17_base.particle.log.log_group import LogGroup

from x17_container.dockers.image.imagebuild import ImageBuild
from x17_container.dockers.image.imageaction import ImageAction
from x17_container.dockers.image.imagetype import ImageType


class Image:
    
    @classmethod
    def from_docker(
        cls,
        docker_client: DockerClient,
        docker_image: DockerImage,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        verbose: bool = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
        **kwargs: Any, # additional parameters
    ) -> "Image":
        image = cls(
            docker_client=docker_client, 
            docker_image=docker_image,
            name=name,
            action=ImageAction(mode="MANUAL"),
            tags=tags or [],
            verbose=verbose,
            log_stream=log_stream or LogStream(
                group=log_group,
                name=name or docker_image.id,
                verbose=verbose,
            ),
            **kwargs,
        )
        return image
    
    @classmethod
    def from_dict(
        cls,
        docker_client: DockerClient,
        data: Dict[str, Any],
        verbose: bool = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
        **kwargs: Any, # additional parameters
    ):
        image = cls(
            docker_client=docker_client,
            name=data.get("name"),
            remote=data.get("remote"),
            build=data.get("imagebuild"),
            action=ImageAction.from_str(
                data.get("action", "AUTOMATIC"),
            ),
            tags=data.get("tags", []),
            verbose=verbose,
            log_stream=log_stream,
            log_group=log_group,
            **kwargs,
        )
        image.load_attrs()
        return image
    
    
    def __init__(
        self, 
        docker_client: Optional[DockerClient] = None, 
        docker_image: Optional[DockerImage] = None,
        remote: Optional[str] = None, # base image to pull or build from
        name: Optional[str] = None, # name for build or custom image
        build: Optional[ImageBuild | Dict[str, Any]] = None,
        action: Optional[ImageAction | str] = None,
        verbose: bool = False,
        log_stream: Optional[LogStream] = None,
        log_group: Optional[LogGroup] = None,
        skip: bool = False,
        **kwargs: Any, # additional parameters
    ):      
        # Initialize Docker client and image attributes
        self.docker_client = docker_client or docker.from_env()
        self.docker_image = docker_image
        self.verbose = verbose
        if log_stream:
            self.log_stream = log_stream
        else:
            self.log_stream = LogStream(
                group=log_group,
                name=name,
                verbose=self.verbose,
            )
        
        # Initialize base image attributes [basic]
        self.name: Optional[str] = name
        self.remote: Optional[str] = remote
        self.id: Optional[str] = None
        self.labels: Dict[str, Any] = {}
        self.repotags: List[str] = []
        self.repodigests: List[str] = []
        self.parent: Optional[str] = None
        self.comment: Optional[str] = None
        self.created: Optional[str] = None
        self.docker_version: Optional[str] = None
        self.author: Optional[str] = None
        self.config: Dict[str, Any] = {}
        self.architecture: Optional[str] = None
        self.variant: Optional[str] = None
        self.os: Optional[str] = None
        self.size: int = 0
        self.graph_driver: Dict[str, Any] = {}
        self.rootfs = {}
        self.metadata = {}
        self.descriptor = {}
        
        # Initialize custom image attributes [advanced]
        if isinstance(build, ImageBuild):
            self.imagebuild = build
        elif isinstance(build, dict):
            self.imagebuild = ImageBuild(params=build)
        else:
            self.imagebuild = None
        
        if isinstance(action, ImageAction):
            self.action = action
        elif isinstance(action, str):
            self.action = ImageAction.from_str(action)
        else:
            self.action = ImageAction(mode="AUTOMATIC")
        
        if not self.name:
            if self.image_type == ImageType.SINGLETON and self.remote:
                self.name = self.remote
            else:
                self.name = None
        
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)
    
        # Initialize Docker image attributes
        if skip:
            self.log_stream.info(f"Skipping setup for image '{self.name}'")
            self.load_attrs()
        else:
            self.setup()

    @property
    def status(self) -> str:
        if self.exists():
            return "AVAILABLE"
        else:
            return "NOT_FOUND"
        
    @property
    def repository(self) -> Optional[str]:
        if self.name:
            return self.name.split(":")[0].strip()
        return None
    
    @property
    def tag(self) -> Optional[str]:
        if self.name and ":" in self.name:
            return self.name.split(":")[1].strip()
        return None
        
    @property
    def full_status(self) -> str:
        return f"[{self.status.upper()}] {self.name or self.id} ({self.size})"
    
    @property 
    def image_type(self) -> ImageType:
        if not self.remote and not self.imagebuild and self.docker_image:
            return ImageType.LOADED
        elif self.remote and self.imagebuild:
            return ImageType.HYBRID
        elif self.remote and not self.imagebuild:
            return ImageType.SINGLETON
        elif not self.remote and self.imagebuild:
            return ImageType.CUSTOM
        else:
            return ImageType.UNKNOWN

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "id": self.id,
            "remote": self.remote,
            "image_type": self.image_type,
            "status": self.status,
            "full_status": self.full_status,
            "imagebuild": self.imagebuild.dict if self.imagebuild else {},
            "action": self.action.dict if self.action else {},
            "tags": self.tags,
            "labels": self.labels,
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

    def __str__(self) -> str:
        return self.name or self.id or "Unknown Image"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, id={self.id})"
    
    def setup(self) -> "Image":
        if self.action.is_manual:
            self.log_stream.info(f"Skipping image setup for '{self.name}' [{self.action}]")
            self.load_attrs()
        else:
            self.log_stream.info(f" Setting up image '{self.name}' [{self.action}]")
            if self.action.to_pull and not self.action.is_build:
                if self.action.is_automatic:
                    self.pull(force=False, check=False)
                else:
                    self.pull(force=False, check=True)
            if self.action.to_build and not self.action.is_pull:
                if self.action.is_automatic:
                    self.build(check=False)
                else:
                    self.build(check=True)
        return self

    def load_attrs(self) -> "Image":
        if self.docker_image:
            self.labels = self.docker_image.labels or {}
            self.tags = self.docker_image.tags or []
            if hasattr(self.docker_image, 'attrs'):
                raw_attributes = self.docker_image.attrs
            else:
                raw_attributes = {}
        else:
            self.labels = {}
            self.tags = []
            raw_attributes = {}
            
        if hasattr(self.docker_image, 'id'):
            self.id = self.docker_image.id
        else:
            self.id = raw_attributes.get("Id", None)
            
        self.repotags = raw_attributes.get("RepoTags", [])
        self.repodigests = raw_attributes.get("RepoDigests", [])
        self.parent = raw_attributes.get("Parent")
        self.comment = raw_attributes.get("Comment")
        self.created = raw_attributes.get("Created")
        self.docker_version = raw_attributes.get("DockerVersion")
        self.author = raw_attributes.get("Author")
        self.config = raw_attributes.get("Config", {})
        self.architecture = raw_attributes.get("Architecture")
        self.variant = raw_attributes.get("Variant")
        self.os = raw_attributes.get("Os")
        self.size = raw_attributes.get("Size", 0)
        self.graph_driver = raw_attributes.get("GraphDriver", {})
        self.rootfs = raw_attributes.get("RootFS", {})
        self.metadata = raw_attributes.get("Metadata", {})
        self.descriptor = raw_attributes.get("Descriptor", {})
        return self

    def exists_remote(self) -> bool:
        try:
            self.docker_client.images.get(self.remote)
            return True
        except (docker.errors.ImageNotFound, docker.errors.APIError) as e:
            return False
    
    def delete_remote(
        self, 
        force: Optional[bool] = False,
        check: Optional[bool] = False,
    ) -> "Image":
        try:
            self.docker_client.images.remove(self.remote, force=force)
            self.log_stream.info(f"Remote image '{self.remote}' deleted successfully.")
        except Exception as error:
            if check:
                raise RuntimeError(f"Failed to delete remote image '{self.remote}': {str(error)}")
            else:
                self.log_stream.info(f"Failed to delete remote image '{self.remote}', but continuing: {str(error)}")
        self.docker_image = None
        self.load_attrs()
        return self
       
    def delete_build(
        self,
        force: Optional[bool] = False,
        check: Optional[bool] = False,
    ) -> "Image":
        try:
            self.docker_client.images.remove(self.name or self.id, force=force)
            self.log_stream.info(f"Custom image '{self.name}' deleted successfully.")
        except Exception as error:
            if check:
                raise RuntimeError(f"Failed to delete custom image '{self.name}': {str(error)}")
            else:
                self.log_stream.info(f"Failed to delete custom image '{self.name}', but continuing: {str(error)}")
        self.docker_image = None
        self.load_attrs()
        return self
            
    def delete(
        self,
        force: Optional[bool] = False,
        check: Optional[bool] = False,
    ):
        if self.exists():
            if self.remote and self.exists_remote():
                return self.delete_remote(force=force, check=check)
            elif self.imagebuild and self.exists_build():
                return self.delete_build(force=force, check=check)
            else:
                return self
        else:
            self.log_stream.info(f"Image '{self.name}' does not exist.")
            if check:
                raise ValueError(f"Nothing to delete.")
            else:
                return self
                
    def pull(
        self,
        force: Optional[bool] = False,
        check: Optional[bool] = True,
    ) -> "Image":
        if not self.remote:
            if check:
                self.log_stream.info("No 'remote' value set")
                raise ValueError("'remote' must be set to pull an image.")
            else:
                self.log_stream.info("No 'remote' value set, skipping pull.")
                return self
        else:
            remote_exists = self.exists_remote()
            if remote_exists:
                self.docker_image = self.docker_client.images.get(self.remote)
                self.load_attrs()
                if force:
                    self.delete_remote(force=True)
                else:
                    self.log_stream.info(f"Image {self.remote} already exists, skipping.")
                    return self
            if not remote_exists:
                self.log_stream.info(f"Pulling image {self.remote}.")
                try:
                    self.docker_image = self.docker_client.images.pull(self.remote)
                    self.load_attrs()
                    self.log_stream.log(f"Image '{self.remote}' pulled successfully.")
                except Exception as error:
                    self.log_stream.log(str(error), level="ERROR")
                    if check:
                        raise RuntimeError(f"Failed to pull image {self.remote}: {str(error)}")
        return self
    
    def build(
        self,
        check: Optional[bool] = True,
    ) -> "Image":
        self.log_stream.info(f"Building image {self.name}.")
        try:
            conf = self.imagebuild.dict.copy()
            if not conf.get("tag"):
                conf["tag"] = self.name
            image, _ = self.docker_client.images.build(**conf)
            self.docker_image = image
            self.log_stream.info(f"Image {self.name} built successfully.")
        except Exception as e:
            if check:
                self.log_stream.log(f"Failed to build image '{self.name}': {str(e)}", level="ERROR")
                raise RuntimeError("Build failed: " + str(e))
            else:
                self.log_stream.log(f"Build failed for image '{self.name}', but continuing: {str(e)}", level="WARNING")
        self.load_attrs()
        return self

    def exists_build(self) -> bool:
        try:
            self.docker_client.images.get(self.name or self.id)
            return True
        except docker.errors.ImageNotFound:
            return False

    def exists(self) -> bool:
        if self.image_type == ImageType.LOADED:
            return True if self.docker_image else False
        elif self.image_type == ImageType.UNKNOWN:
            return False
        else:
            if self.image_type == ImageType.HYBRID:
                return self.exists_remote() and self.exists_build()
            elif self.image_type == ImageType.SINGLETON:
                return self.exists_remote()
            elif self.image_type == ImageType.CUSTOM:
                return self.exists_build()
            else:
                return False

    def export(
        self,
    ) -> Dict[str, Any]:
        return self.dict

    def add_tag(
        self,
        tag: str,
        repository: Optional[str] = None,
        force: bool = True,
        check: Optional[bool] = True,
    ) -> "Image":
        repo = repository or self.repository
        try:
            self.docker_image.tag(
                repository=repo,
                tag=tag,
                force=force,
            )
            self.tags = self.docker_image.tags or []
            self.log_stream.info(f"Tagged image as '{repo}:{tag}'")
        except Exception as error:
            self.log_stream.log(f"Tagging failed: {str(error)}", level="ERROR")
            if check:
                raise

        return Image.from_docker(
            docker_client=self.docker_client,
            docker_image=self.docker_client.images.get(f"{repo}:{tag}"),
            name=f"{repo}:{tag}",
        )
    
    def delete_tag(
        self,
        tag: str,
        repository: Optional[str] = None,
        force: bool = True,
        check: bool = True,
    ) -> bool:
        repo = repository or self.repository
        image_ref = f"{repo}:{tag}" if tag else repo
        try:
            self.docker_client.images.remove(image=image_ref, force=force)
            self.log_stream.info(f"Removed image tag: {image_ref}")
            return True
        except docker.errors.ImageNotFound:
            self.log_stream.warn(f"Image tag not found: {image_ref}")
            return False
        except Exception as error:
            self.log_stream.log(f"Failed to remove tag '{image_ref}': {str(error)}", level="ERROR")
            if check:
                raise
            return False
        