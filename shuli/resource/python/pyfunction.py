# -*- coding: utf-8 -*-
from typing import List, Optional
import ast

from shuli.base.x_function import Function
from shuli.resource.python.pyargument import PyArgument
from shuli.resource.python.pycodeblock import PyCodeBlock


class PyFunction(Function):
    """
    A Python-specific Function Node.
    Supports AST parsing and structured children.
    """

    @classmethod
    def from_ast(cls, node: ast.FunctionDef, code: Optional[str] = None) -> "PyFunction":
        arguments = PyArgument.from_ast(node.args)
        body = PyCodeBlock.from_ast(node, code=code) if code else None
        return cls(
            name=node.name,
            arguments=arguments,
            return_type=ast.unparse(node.returns) if node.returns else None,
            docstring=ast.get_docstring(node),
            start_line=getattr(node, "lineno", None),
            end_line=getattr(node, "end_lineno", None),
            start_column=getattr(node, "col_offset", None),
            end_column=getattr(node, "end_col_offset", None),
            body=body,
        )

    def __init__(
        self,
        name: str,
        arguments: List[PyArgument],
        return_type: Optional[str] = None,
        docstring: Optional[str] = None,
        body: Optional[PyCodeBlock] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        start_column: Optional[int] = None,
        end_column: Optional[int] = None,
    ):
        children = []
        children.extend(arguments)
        if body:
            children.append(body)

        super().__init__(
            name=name,
            return_type=return_type,
            docstring=docstring,
            attributes={
                "start_line": start_line,
                "end_line": end_line,
                "start_column": start_column,
                "end_column": end_column,
            },
            children=children,
        )
        self.arguments = arguments
        self.body = body
        self.start_line = start_line
        self.end_line = end_line
        self.start_column = start_column
        self.end_column = end_column