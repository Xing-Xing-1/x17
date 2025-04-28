# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, Any

from shuli.base.x_codeblock import CodeBlock

class PyCodeBlock(CodeBlock):
    def __init__(
        self,
        name: str,
        arguments: Optional[List[str]] = None,
        body: Optional[CodeBlock] = None,
        docstring: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            arguments=arguments or [],
            body=body or CodeBlock(),
            docstring=docstring,
        )