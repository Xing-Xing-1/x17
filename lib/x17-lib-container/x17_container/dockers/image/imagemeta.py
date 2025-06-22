from typing import Optional, Dict, List, Any


class ImageMeta:
    
    @classmethod
    def from_dict(
        cls, 
        params: Dict[str, Any],
    ) -> "ImageMeta":
        return cls(
            params=params,
            repotags=params.get("repotags", []),
            repodigests=params.get("repodigests", []),
            parent=params.get("parent"),
            comment=params.get("comment"),
            created=params.get("created"),
            docker_version=params.get("docker_version"),
            author=params.get("author"),
            config=params.get("config", {}),
            architecture=params.get("architecture"),
            variant=params.get("variant"),
            os=params.get("os"),
            size=params.get("size", 0),
            graph_driver=params.get("graph_driver", {}),
            rootfs=params.get("rootfs", {}),
            metadata=params.get("metadata", {}),
            descriptor=params.get("descriptor", {}),
        )
    
    def __init__(
        self,
        params: Optional[Dict[str, Any]] = None,
        repotags: Optional[List[str]] = None,
        repodigests: Optional[List[str]] = None,
        parent: Optional[str] = None,
        comment: Optional[str] = None,
        created: Optional[str] = None,
        docker_version: Optional[str] = None,
        author: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        architecture: Optional[str] = None,
        variant: Optional[str] = None,
        os: Optional[str] = None,
        size: int = 0,
        graph_driver: Optional[Dict[str, Any]] = None,
        rootfs: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        descriptor: Optional[Dict[str, Any]] = None,
    ):
        if params is not None:
            self.repotags = params.get("repotags", [])
            self.repodigests = params.get("repodigests", [])
            self.parent = params.get("parent")
            self.comment = params.get("comment")
            self.created = params.get("created")
            self.docker_version = params.get("docker_version")
            self.author = params.get("author")
            self.config = params.get("config", {})
            self.architecture = params.get("architecture")
            self.variant = params.get("variant")
            self.os = params.get("os")
            self.size = params.get("size", 0)
            self.graph_driver = params.get("graph_driver", {})
            self.rootfs = params.get("rootfs", {})
            self.metadata = params.get("metadata", {})
            self.descriptor = params.get("descriptor", {})
        else:
            self.repotags = repotags or []
            self.repodigests = repodigests or []
            self.parent = parent
            self.comment = comment
            self.created = created
            self.docker_version = docker_version
            self.author = author
            self.config = config or {}
            self.architecture = architecture
            self.variant = variant
            self.os = os
            self.size = size
            self.graph_driver = graph_driver or {}
            self.rootfs = rootfs or {}
            self.metadata = metadata or {}
            self.descriptor = descriptor or {}
            
    @property
    def dict(self) -> Dict[str, Any]:
        return {
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
        return ", ".join(self.repotags)

    def __repr__(self):
        attributes = []
        for unit, value in self.dict.items():
            attributes.append(f"{unit}={value}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def is_valid(self) -> bool:
        for key in self.dict:
            if self.dict[key]:
                return True
        return False

    def export(self) -> Dict[str, Any]:
        return self.dict