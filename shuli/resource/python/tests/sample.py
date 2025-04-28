# sample.py

import os
import sys
from typing import List, Dict

CONSTANT = 42

class BaseClass:
    """This is a base class."""
    def base_method(self, value: int) -> int:
        """Base method"""
        return value

class ChildClass(BaseClass):
    """This is a child class inheriting BaseClass."""

    class InnerClass:
        """Nested class inside another class."""
        pass

    def __init__(self, name: str):
        self.name = name

    def child_method(self, param: str) -> str:
        """Child method"""
        return param

def standalone_function(x: int, y: int = 10) -> int:
    """A standalone function outside classes."""
    return x + y

async def async_function(data: List[int]) -> List[int]:
    """An asynchronous function."""
    return [i * 2 for i in data]