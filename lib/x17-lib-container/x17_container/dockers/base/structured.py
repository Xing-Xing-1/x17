from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


class Structured:

    @classmethod
    def from_dict(
        cls,
        data: Optional[Dict[str, Any]] = None,
    ) -> "Structured":
        return cls(**(data or {}))

    def __init__(self, **kwargs: Any):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def set(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        def _serialize(obj: Any) -> Any:
            if isinstance(obj, Structured):
                return obj.to_dict()
            elif isinstance(obj, list):
                return [_serialize(v) for v in obj]
            elif isinstance(obj, dict):
                return {k: _serialize(v) for k, v in obj.items()}
            elif isinstance(obj, datetime):
                return obj.isoformat()
            else:
                return obj

        return {key: _serialize(value) for key, value in self.__dict__.items()}

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Structured):
            return self.to_dict() == other.to_dict()
        if isinstance(other, dict):
            return self.to_dict() == other
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        def normalize(obj):
            if isinstance(obj, dict):
                return tuple(sorted((k, normalize(v)) for k, v in obj.items()))
            elif isinstance(obj, list):
                return tuple(normalize(v) for v in obj)
            elif isinstance(obj, Structured):
                return normalize(obj.to_dict())
            else:
                return obj

        return hash(normalize(self.to_dict()))

    def copy(self, **overrides: Any) -> "Structured":
        data = self.__dict__.copy()
        data.update(overrides)
        return self.__class__(**data)
