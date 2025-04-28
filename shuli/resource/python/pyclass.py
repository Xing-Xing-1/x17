# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, Any

from shuli.base.x_class import Class

class PyClass(Class):
    
    def __init__(
        self,
        name: str,
        bases: Optional[List[str]] = None,
        attributes: Optional[List[str]] = None,
        methods: Optional[List[str]] = None,
        docstring: Optional[str] = None,
        body: Optional[Any] = None,
    ):
        super().__init__(
            name=name,
            bases=bases,
            attributes=attributes,
            methods=methods,
            docstring=docstring,
            body=body,
        )
        
        