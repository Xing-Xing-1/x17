# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, Any

from shuli.base.x_function import Function

class PyFunction(Function):
    def __init__(
        self,
        name: str,
        arguments: Optional[List[str]] = None,
        return_type: Optional[str] = None,
        docstring: Optional[str] = None,
        body: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            arguments=arguments or [],
            return_type=return_type,
            docstring=docstring,
            body=body or "",
        )