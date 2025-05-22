# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional
import warnings


class Semistruct(dict):
    
    def __init__(
        self, 
        data: Optional[Dict[str, Any]] = None,
        name: Optional[str] = "",
    ):
        super().__init__(data or {})
        self.name = name
        
    @property
    def attr(self) -> list[str]:
        return [
            key for key in self.__dict__.keys() 
            if not key.startswith("_") and isinstance(self.__dict__[key], str)
        ]
    
    @property
    def dict(self) -> Dict[str, str]:
        return {key: getattr(self, key) for key in self.attr}

    def __repr__(self):
        attr_parts = []
        for key in self.attr:
            value = getattr(self, key, None)
            attr_parts.append(f"{key}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(attr_parts)})"
    
    def __str__(self):
        return self.name 
    
    def put(self, key: str, value: Any) -> None:
        super().__setitem__(key, value)
        return self
        
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return super().get(key, default)
    
    def remove(self, key: str) -> None:
        if key in self:
            del self[key]
            
    def update(self, other: Dict[str, Any]) -> None:
        for k, v in other.items():
            self[k] = v
            
    # --- Forbidded native methods ---

    def warn(
        self,
        message: str,
        category: type = UserWarning,
        stacklevel: int = 2,
    ):
        warnings.warn(message, category=category, stacklevel=stacklevel)

    def __getitem__(self, key):
        self.warn(f"direct access obj[{key!r}] is disabled. Use .get({key!r})",)

    def __setitem__(self, key, value):
        self.warn(f"direct assignment obj[{key!r}] = {value!r} is disabled. Use .put({key!r}, {value!r}).")

    def update(self, *args, **kwargs):
        self.warn("update() is disabled. Use .merge().")

    def pop(self, *args, **kwargs):
        self.warn("pop() is disabled. Use .remove().")

    
    