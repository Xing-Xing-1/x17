# -*- coding: utf-8 -*-
from typing import List, Optional, Dict, Any
import ast

from shuli.resource.python.pynode import PyNode
from shuli.base.nodetype import NodeType


class PyArgument(PyNode):
    """
    A Python-specific Argument Node.
    Extends the generic Argument particle,
    adding parsing capability from AST for function arguments.

    """

    @classmethod
    def from_ast(
        cls,
        astnode: ast.arg | ast.arguments,
        name: Optional[str] = None,
    ) -> List["PyArgument"]:
        arguments = []
        if isinstance(astnode, ast.arg):
            arguments.extend(cls.from_ast_arg(astnode, name=name))
        if isinstance(astnode, ast.arguments):
            arguments.extend(cls.from_ast_arguments(astnode))
        return arguments

    @classmethod
    def from_ast_arg(
        cls,
        astnode: ast.arg,
        name: Optional[str] = None,
        default: Optional[str] = None,
        is_vararg: bool = False,
        is_kwarg: bool = False,
        is_kwonly: bool = False,
        is_posonly: bool = False,
    ) -> List["PyArgument"]:
        return [cls(
            astnode=astnode,
            name=getattr(astnode, "arg", None) or name,
            attributes={
                "asttype": astnode.__class__.__name__,
                "annotation": PyNode.unparse(getattr(astnode, "annotation", None)),
                "type_comment": PyNode.unparse(getattr(astnode, "type_comment", None)),
                "default": default,
                "is_vararg": is_vararg,
                "is_kwarg": is_kwarg,
                "is_kwonly": is_kwonly,
                "is_posonly": is_posonly,
                "start_line": getattr(astnode, "lineno", None),
                "end_line": getattr(astnode, "end_lineno", None),
                "start_col": getattr(astnode, "col_offset", None),
                "end_col": getattr(astnode, "end_col_offset", None),
            }
        )]

    @classmethod
    def from_ast_arguments(
        cls,
        astnode: ast.arguments,
    ) -> List["PyArgument"]:
        arguments = []
        positional_args = astnode.posonlyargs + astnode.args
        defaults = [None] * (len(positional_args) - len(astnode.defaults)) + astnode.defaults

        for arg_node, default_node in zip(positional_args, defaults):
            default = PyNode.unparse(default_node, fallback=["value", "id"])
            arguments.extend(cls.from_ast_arg(arg_node, default=default, is_posonly=True))

        if astnode.vararg:
            arguments.extend(cls.from_ast_arg(astnode.vararg, is_vararg=True))

        for kwarg_node, kw_default_node in zip(astnode.kwonlyargs, astnode.kw_defaults):
            default = PyNode.unparse(kw_default_node, fallback=["value", "id"])
            arguments.extend(cls.from_ast_arg(kwarg_node, default=default, is_kwonly=True))

        if astnode.kwarg:
            arguments.extend(cls.from_ast_arg(astnode.kwarg, is_kwarg=True))

        return arguments


    def __init__(
        self,
        astnode: ast.arg | ast.arguments,
        name: str,
        attributes: Optional[Dict[str, Any]] = {},
    ):
        super().__init__(
            astnode=astnode,
            type=NodeType.ARGUMENT,
            name=name,
            attributes=attributes,
        )
        self.astnode = astnode

