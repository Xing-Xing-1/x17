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

    def __init__(self, validate_fields: bool = True, **kwargs: Any):
        for key, value in kwargs.items():
            if validate_fields:
                self.validate_field(self, key, value)
            setattr(self, key, value)

    def validate_field(
        self, 
        key: str, 
        value: Any, 
        path: str = "",
    ) -> None:
        from x17_container.dockers.base.configuration import Configuration
        from x17_container.dockers.base.attributes import Attributes

        full_path = f"{path}.{key}" if path else key
        primitive_types = (int, float, str, bool, type(None), datetime)
        
        if isinstance(value, primitive_types):
            return
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                self.validate_field(f"[{idx}]", item, path=full_path)
        elif isinstance(value, dict):
            for k, v in value.items():
                self.validate_field(k, v, path=full_path)
        elif isinstance(value, Structured):
            if not isinstance(value, (Configuration, Attributes)):
                raise TypeError(f"Disallowed Structured subclass at '{full_path}': {type(value).__name__}")
            for k, v in value.__dict__.items():
                self.validate_field(k, v, path=full_path)
        else:
            raise TypeError(f"Illegal type at '{full_path}': {type(value).__name__}")
    
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
