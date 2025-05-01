# -*- coding: utf-8 -*-
from typing import List, Optional
import ast

from shuli.resource.python.pynode import PyNode

class PyFunction(PyNode):
    """
    A Python-specific Function Node.
    Supports AST parsing and structured children.
    
    # """
    pass
    
    # @classmethod
    # def from_ast(
    #     cls, 
    #     node: ast.FunctionDef,
    # ) -> "PyFunction":
    #     try:
    #         code = ast.unparse(node)
    #     except Exception:
    #         code = ''
    #     arguments = PyArgument.from_ast(node.args)
    #     docstring = ast.get_docstring(node)
    #     body = PyCodeBlock.from_ast(node)
    #     return_type = ast.unparse(node.returns) if node.returns else None
    #     return cls(
    #         name=node.name,
    #         arguments=arguments,
    #         docstring=docstring,
    #         body=body,
    #         return_type=return_type,
    #         start_line=getattr(node, "lineno", None),
    #         end_line=getattr(node, "end_lineno", None),
    #         start_column=getattr(node, "col_offset", None),
    #         end_column=getattr(node, "end_col_offset", None),
    #     )

    # def __init__(
    #     self,
    #     name: str,
    #     arguments: List[PyArgument] = [],
    #     docstring: Optional[str] = None,
    #     body: Optional[PyCodeBlock] = None,
    #     return_type: Optional[str] = None,
    #     start_line: Optional[int] = None,
    #     end_line: Optional[int] = None,
    #     start_column: Optional[int] = None,
    #     end_column: Optional[int] = None,
    #     astnode: Optional[ast.FunctionDef] = None,
    # ):
    #     children = []
    #     children.extend(arguments)
    #     if body:
    #         children.append(body)

    #     super().__init__(
    #         name=name,
    #         return_type=return_type,
    #         docstring=docstring,
    #         attributes={
    #             "start_line": start_line,
    #             "end_line": end_line,
    #             "start_column": start_column,
    #             "end_column": end_column,
    #         },
    #         children=children,
    #     )
    #     self.arguments = arguments
    #     self.body = body
    #     self.start_line = start_line
    #     self.end_line = end_line
    #     self.start_column = start_column
    #     self.end_column = end_column
    #     self.astnode = astnode
        
        
        
    # @property
    # def code(self) -> str:
    #     try:
    #         code = ast.unparse(self.astnode)
    #     except Exception:
    #         code = ''
    #     return code
    
    