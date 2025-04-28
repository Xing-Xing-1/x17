# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, Any

from shuli.base.x_argument import Argument

class PyArgument(Argument):
    def __init__(
        self, 
        name: str, 
        type_hint: Optional[str] = None, 
        default: Optional[Any] = None,
    ):
        super().__init__(
            name=name, 
            type_hint=type_hint, 
            default=default,
        )
    