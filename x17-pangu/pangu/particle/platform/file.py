from typing import Optional

from pangu.particle.platform.path import Path


class File:
    def __init__(self, path: Path):
        self.path = path
    
    def __str__(self) -> str:
        return str(self.path)
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path={self.path})"

    def read(self) -> str:
        raise NotImplementedError("read() must be implemented by subclass")

    def write(self, content: str):
        raise NotImplementedError("write() must be implemented by subclass")

    def exists(self) -> bool:
        raise NotImplementedError("exists() must be implemented by subclass")


