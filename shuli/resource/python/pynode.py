# -*- coding: utf-8 -*-
import ast
from typing import Optional, List, Dict, Any

from shuli.base.node import Node
from shuli.base.nodetype import NodeType


class PyNode(Node):
    """
    A Python-specific Node extended from base Node.
    Wraps an ast.AST node and builds a tree of PyNode children.
    
    """
    @classmethod
    def from_ast(
        cls,
        astnode: ast.AST,
        type: NodeType = NodeType.UNKNOWN,
        name: Optional[str] = None,
    ) -> "PyNode":
        name = name or getattr(astnode, "name", None)
        attributes = {
            "asttype": astnode.__class__.__name__,
            "start_line": getattr(astnode, "lineno", None),
            "end_line": getattr(astnode, "end_lineno", None),
            "start_col": getattr(astnode, "col_offset", None),
            "end_col": getattr(astnode, "end_col_offset", None),
        }
        node = cls(
            astnode=astnode, 
            name=name,
            type=type,
            attributes=attributes,
        )
        for child in ast.iter_child_nodes(astnode):
            if isinstance(child, ast.AST):
                for child_node in cls.from_ast(child):
                    node.add_child(child_node)
        return [node]

    def __init__(
        self,
        astnode: ast.AST,
        type: NodeType = NodeType.UNKNOWN,
        name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        children: Optional[List["PyNode"]] = None,
    ):
        super().__init__(
            type=type,
            name=name,
            attributes=dict(sorted(attributes.items())),
            children=children or [],
        )
        self.astnode = astnode

    @property
    def code(self) -> str:
        try:
            return ast.unparse(self.astnode)
        except Exception:
            return ""

    def export(self) -> Dict[str, Any]:
        result = self.dict.copy()
        if self.children:
            result["children"] = [
                child.export() for child in self.children
            ]
        return result
    
