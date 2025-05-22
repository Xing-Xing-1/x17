from abc import ABC, abstractmethod


class Path(ABC):
    def __init__(self, raw: str):
        self.raw = raw

    def __str__(self) -> str:
        return str(self.raw)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(raw={self.raw})"

    @abstractmethod
    def is_absolute(self) -> bool: 
        raise NotImplementedError("Subclasses must implement to_uri method.")

    @abstractmethod
    def is_remote(self) -> bool:
        raise NotImplementedError("Subclasses must implement to_uri method.")

    @abstractmethod
    def to_uri(self) -> str:
        raise NotImplementedError("Subclasses must implement to_uri method.")

    def export(self) -> dict:
        return {
            "raw": self.raw,
        }
