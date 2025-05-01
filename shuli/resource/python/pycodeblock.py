# -*- coding: utf-8 -*-
from typing import Optional
import ast

from shuli.resource.python.pynode import PyNode

class PyCodeBlock(PyNode):
    """
    A Python-specific CodeBlock Node.
    Represents a chunk of code from AST nodes or raw code.
    """
    pass
    
    
    # @classmethod
    # def from_ast(
    #     cls,
    #     node: ast.AST,
    # ) -> "PyCodeBlock":
    #     start_line = getattr(node, "lineno", None)
    #     end_line = getattr(node, "end_lineno", None)
    #     start_column = getattr(node, "col_offset", None)
    #     end_column = getattr(node, "end_col_offset", None)
        
    #     try:
    #         code = ast.unparse(node)
    #     except Exception:
    #         code = None
        
    #     return cls(
    #         content=code or "",
    #         start_line=start_line,
    #         end_line=end_line,
    #         start_column=start_column,
    #         end_column=end_column,
    #         astnode=node,
    #     )

    # def __init__(
    #     self,
    #     content: str,
    #     start_line: Optional[int] = None,
    #     end_line: Optional[int] = None,
    #     start_column: Optional[int] = None,
    #     end_column: Optional[int] = None,
    #     astnode: Optional[ast.AST] = None,
    # ):
    #     super().__init__(
    #         content=content,
    #         attributes={
    #             "start_line": start_line,
    #             "end_line": end_line,
    #             "start_column": start_column,
    #             "end_column": end_column,
    #         }
    #     )
    #     self.start_line = start_line
    #     self.end_line = end_line
    #     self.start_column = start_column
    #     self.end_column = end_column
    #     self.astnode=astnode

    # @property
    # def code(self) -> str:
    #     return ast.unparse(self.astnode) if self.astnode else ""
    