# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, Tuple

class BaseModel():
    def __init__(
        self, 
        name: str,
        interface: Any = None,
    ):
        """
        Initialize the model with the given name and any additional arguments.
        """
        self.name = name

    
    
