# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, Any

from shuli.base.x_import import Import

class PyImport(Import):
    def __init__(
        self, 
        source: str, 
        alias: Optional[str] = None,
    ):
        super().__init__(
            source=source, 
            alias=alias,
        )