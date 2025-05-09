# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any

class BaseInterface(ABC):
    """
    Abstract base interface for all LLM wrappers.
    Provides the minimal API for stateless inference.
    
    """

    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def infer(self, prompt: str, **kwargs) -> str:
        """
        Perform stateless inference on a given prompt.

        """
        pass

    @abstractmethod
    def check_env(self) -> bool:
        """
        Check if the environment is set up correctly for the model.
        This can include checking for required files, directories, or configurations.
        """
        pass