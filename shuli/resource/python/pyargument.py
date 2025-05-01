# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, Any
import ast

from shuli.resource.python.pynode import PyNode

class PyArgument(PyNode):
    """
    A Python-specific Argument Node.
    Extends the generic Argument particle,
    adding parsing capability from AST for function arguments.
    
    """
    pass

#     @classmethod
#     def from_ast(
#         cls,
#         node: ast.arg | ast.arguments,
#     ) -> List["PyArgument"]:
#         arguments = []
#         if isinstance(node, ast.arg):
#             arguments.extend(
#                 cls.from_ast_arg(node)
#             )
#         if isinstance(node, ast.arguments):
#             arguments.extend(
#                 cls.from_ast_arguments(node)
#             )
#         return arguments
    
#     @classmethod
#     def from_ast_arg(
#         cls,
#         node: ast.arg,
#         default: Optional[Any] = None,
#         is_vararg: bool = False,
#         is_kwarg: bool = False,
#         is_kwonly: bool = False,
#     )-> List["PyArgument"]:
#         return [cls(
#             name = getattr(node, "arg", "<unknown>"),
#             type_hint = ast.unparse(node.annotation) if getattr(node, "annotation", None) else None,
#             default=default,
#             is_vararg=is_vararg,
#             is_kwarg=is_kwarg,
#             is_kwonly=is_kwonly,
#             start_line=getattr(node, "lineno", None),
#             end_line=getattr(node, "end_lineno", None),
#             start_column=getattr(node, "col_offset", None),
#             end_column=getattr(node, "end_col_offset", None),
#             astnode=node,
#         )]
    
#     @classmethod
#     def from_ast_arguments(
#         cls,
#         node: ast.arguments,
#     ) -> List["PyArgument"]:
#         """
#         Process the full ast.arguments node.
#         Handles posonlyargs, args, vararg, kwonlyargs, kwarg.
#         """
#         arguments = []
        
#         # --- Process normal positional args ---
#         pos_args = node.posonlyargs + node.args
#         defaults = [None] * (len(pos_args) - len(node.defaults)) + node.defaults

#         for arg_node, default_node in zip(pos_args, defaults):
#             default = ast.unparse(default_node) if default_node is not None else None
#             arguments.extend(cls.from_ast_arg(arg_node, default=default))

#         if node.vararg:
#             arguments.extend(cls.from_ast_arg(
#                 node.vararg, 
#                 is_vararg=True
#             ))

#         kw_defaults = node.kw_defaults
#         for kwarg_node, kw_default_node in zip(node.kwonlyargs, kw_defaults):
#             default = ast.unparse(kw_default_node) if kw_default_node is not None else None
#             arguments.extend(cls.from_ast_arg(
#                 kwarg_node,
#                 default=default,
#                 is_kwonly=True
#             ))

#         if node.kwarg:
#             arguments.extend(cls.from_ast_arg(
#                 node.kwarg, 
#                 is_kwarg=True
#             ))

#         return arguments
    
#     def __init__(
#         self, 
#         name: str, 
#         type_hint: Optional[str] = None, 
#         default: Optional[Any] = None,
#         is_vararg: bool = False,
#         is_kwarg: bool = False,
#         is_kwonly: bool = False,
#         start_line: Optional[int] = None,
#         end_line: Optional[int] = None,
#         start_column: Optional[int] = None,
#         end_column: Optional[int] = None,
#         astnode: Optional[ast.AST] = None,
#     ):
#         super().__init__(
#             name=name, 
#             type_hint=type_hint, 
#             default=default,
#             attributes={
#                 "is_vararg": is_vararg,
#                 "is_kwarg": is_kwarg,
#                 "is_kwonly": is_kwonly,
#                 "start_line": start_line,
#                 "end_line": end_line,
#                 "start_column": start_column,
#                 "end_column": end_column,
#             }
#         )
#         self.is_vararg = is_vararg
#         self.is_kwarg = is_kwarg
#         self.is_kwonly = is_kwonly
#         self.start_line = start_line
#         self.end_line = end_line
#         self.start_column = start_column
#         self.end_column = end_column
#         self.astnode = astnode
    
#     @property
#     def code(self) -> str:
#         return ast.unparse(self.astnode) if self.astnode else ""
        
