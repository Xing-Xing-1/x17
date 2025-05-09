# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

class BaseModel(ABC):
    """
    Base class for all models in the Nvwa framework.
    This class provides the minimal API for model inference, prediction, and evaluation.
    
    """

    def __init__(self, name: str, *args, **kwargs):
        """
        Initialize the model with the given name and any additional arguments.
        """
        super().__init__(*args, **kwargs)
        self.name = name

    @abstractmethod
    def infer(self, prompt: str, *args, **kwargs) -> Dict[str, Any]:
        """
        Perform a single-round inference.
        
        """
        pass

    @abstractmethod
    def predict(self, *args, **kwargs):
        """
        Make predictions with the model using the given arguments.
        """
        pass

    @abstractmethod
    def evaluate(self, *args, **kwargs):
        """
        Evaluate the model with the given arguments.
        """
        pass
