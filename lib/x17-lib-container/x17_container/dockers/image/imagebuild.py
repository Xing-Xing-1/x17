from typing import Optional, Dict, List, Any


class ImageBuild:
    
    @classmethod
    def from_dict(
        cls, 
        params: Dict[str, Any],
    ) -> "ImageBuild":
        params = params or {}
        return cls(
            params=params,
            path=params.get("path"),
            fileobj=params.get("fileobj"),
            tag=params.get("tag") or params.get("name"),
            quiet=params.get("quiet"),
            rm=params.get("rm"),
            timeout=params.get("timeout"),
            custom_context=params.get("custom_context"),
            encoding=params.get("encoding"),
            pull=params.get("pull"),
            forcerm=params.get("forcerm"),
            dockerfile=params.get("dockerfile"),
            buildargs=params.get("buildargs") or {},
            container_limits=params.get("container_limits") or {},
            shmsize=params.get("shmsize"),
            labels=params.get("labels") or {},
            cache_from=params.get("cache_from") or [],
            target=params.get("target"),
            network_mode=params.get("network_mode"),
            squash=params.get("squash"),
            extra_hosts=params.get("extra_hosts") or {},
            platform=params.get("platform"),
            isolation=params.get("isolation"),
            use_config_proxy=params.get("use_config_proxy")
        )
    
    def __init__(
        self,
        params: Optional[Dict[str, Any]] = None,
        # Core build settings
        path: Optional[str] = None,
        fileobj: Optional[Any] = None,
        dockerfile: Optional[str] = None,
        name: Optional[str] = None,
        tag: Optional[str] = None,
        buildargs: Optional[Dict[str, str]] = None,
        # Docker build flags
        quiet: Optional[bool] = None,
        rm: Optional[bool] = None,
        forcerm: Optional[bool] = None,
        pull: Optional[bool] = None,
        timeout: Optional[int] = None,
        custom_context: Optional[bool] = None,
        encoding: Optional[str] = None,
        # Advanced options
        container_limits: Optional[Dict[str, Any]] = None,
        shmsize: Optional[int] = None,
        labels: Optional[Dict[str, str]] = None,
        cache_from: Optional[List[str]] = None,
        target: Optional[str] = None,
        network_mode: Optional[str] = None,
        squash: Optional[bool] = None,
        extra_hosts: Optional[Dict[str, str]] = None,
        platform: Optional[str] = None,
        isolation: Optional[str] = None,
        use_config_proxy: Optional[bool] = None,
    ):
        if params is not None:
            self.path = params.get("path")
            self.fileobj = params.get("fileobj")
            self.tag = params.get("tag") or params.get("name")
            self.quiet = params.get("quiet")
            self.rm = params.get("rm")
            self.timeout = params.get("timeout")
            self.custom_context = params.get("custom_context")
            self.encoding = params.get("encoding")
            self.pull = params.get("pull")
            self.forcerm = params.get("forcerm")
            self.dockerfile = params.get("dockerfile")
            self.buildargs = params.get("buildargs") or {}
            self.container_limits = params.get("container_limits") or {}
            self.shmsize = params.get("shmsize")
            self.labels = params.get("labels")
            self.cache_from = params.get("cache_from") or []
            self.target = params.get("target")
            self.network_mode = params.get("network_mode")
            self.squash = params.get("squash")
            self.extra_hosts = params.get("extra_hosts") or {}
            self.platform = params.get("platform")
            self.isolation = params.get("isolation")
            self.use_config_proxy = params.get("use_config_proxy")
        else:
            self.path = path
            self.fileobj = fileobj
            self.tag = tag or name
            self.quiet = quiet
            self.rm = rm
            self.timeout = timeout
            self.custom_context = custom_context
            self.encoding = encoding
            self.pull = pull
            self.forcerm = forcerm
            self.dockerfile = dockerfile
            self.buildargs = buildargs or {}
            self.container_limits = container_limits or {}
            self.shmsize = shmsize
            self.labels = labels or {}
            self.cache_from = cache_from or []
            self.target = target
            self.network_mode = network_mode
            self.squash = squash
            self.extra_hosts = extra_hosts or {}
            self.platform = platform
            self.isolation = isolation
            self.use_config_proxy = use_config_proxy

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "fileobj": self.fileobj,
            "tag": self.tag,
            "quiet": self.quiet,
            "rm": self.rm,
            "timeout": self.timeout,
            "custom_context": self.custom_context,
            "encoding": self.encoding,
            "pull": self.pull,
            "forcerm": self.forcerm,
            "dockerfile": self.dockerfile,
            "buildargs": self.buildargs,
            "container_limits": self.container_limits,
            "shmsize": self.shmsize,
            "labels": self.labels,
            "cache_from": self.cache_from,
            "target": self.target,
            "network_mode": self.network_mode,
            "squash": self.squash,
            "extra_hosts": self.extra_hosts,
            "platform": self.platform,
            "isolation": self.isolation,
            "use_config_proxy": self.use_config_proxy
        }

    def __str__(self):
        return self.path

    def __repr__(self):
        attributes = []
        for unit, value in self.dict.items():
            attributes.append(f"{unit}={value}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def is_valid(self) -> bool:
        return self.path is not None or self.fileobj is not None

    def export(self) -> Dict[str, Any]:
        return self.dict
