#!/usr/bin/python
# -*- coding: utf-8 -*-
from pangu.particle.constant.hash import HASH_ALGORITHMS
import fnmatch

class Text:
    def __init__(
        self,
        content: str = "",
    ):
        self.content = content

    @property
    def dict(self):
        return {
            "content": self.content,
        }

    def __str__(self) -> str:
        return self.content
    
    def __len__(self) -> int:
        return len(self.content)
    
    def __repr__(self) -> str:
        attributes = []
        for unit, value in self.dict.items():
            if value:
                if len(value) > 10: value = f"{value[:10]}..."
                attributes.append(f"{unit}={value}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"
    
    # --- operators ---
    def __add__(self, other) -> str:
        if isinstance(other, str):
            return Text(self.content + other)
        if isinstance(other, Text):
            return Text(self.content + other.content)
        raise TypeError(f"Unsupported type for addition: {type(other)}")
    
    def __radd__(self, other) -> str:
        if isinstance(other, str):
            return Text(other + self.content)
        if isinstance(other, Text):
            return Text(other.content + self.content)
        raise TypeError(f"Unsupported type for addition: {type(other)}")
    
    def __eq__(self, value):
        if isinstance(value, str):
            return self.content == value
        if isinstance(value, Text):
            return self.content == value.content
        raise TypeError(f"Unsupported type for equality: {type(value)}")
    
    def __ne__(self, value):
        if isinstance(value, str):
            return self.content != value
        if isinstance(value, Text):
            return self.content != value.content
        raise TypeError(f"Unsupported type for inequality: {type(value)}")
    
    def __upper__(self) -> str: 
        return self.content.upper()
    
    def __lower__(self) -> str:
        return self.content.lower()
    
    def as_upper(self):
        self.content = self.content.upper()
        
    def as_lower(self):
        self.content = self.content.lower()
    
    def encode(self):
        return self.content.encode()
    
    def as_digest(
        self,
        algorithm: str = "sha256",
    ):
        hash_function = HASH_ALGORITHMS[algorithm]
        hash_function.update(self.encode())
        self.content = hash_function.hexdigest()

    def to_digest(
        self,
        algorithm: str = "sha256",
    ):
        self.as_digest(algorithm)
        return Text(self.content)
    
    def wildcard_match(
        self,
        wildcard: str,
    ):  
        return fnmatch.fnmatch(self.content, wildcard)
    
    