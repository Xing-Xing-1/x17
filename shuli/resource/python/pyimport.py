# -*- coding: utf-8 -*-
from typing import List, Optional, Dict, Any
import ast
import asttokens

from shuli.base.x_import import Import
from shuli.base.x_node import NodeType

class PyImport(Import):
    """
    A Python-specific Import Node.
    Extends the generic Import particle,
    adding parsing capability from AST, 
    and collects detailed information.
    
    """
    
    @classmethod
    def from_ast(
        cls, 
        node: ast.ImportFrom | ast.Import,
    ) -> Optional[List["PyImport"]]:
        imports = []
        names = getattr(node, "names", [])
        for name in names:
            imports.append(
                PyImport(
                    name = name.name,
                    module = getattr(node, "module", None),
                    alias = name.asname,
                    level = getattr(node, "level", None),
                    start_line = getattr(node, "lineno", None),
                    end_line = getattr(node, "end_lineno", None),
                    start_column = getattr(node, "col_offset", None),
                    end_column = getattr(node, "end_col_offset", None),
                )
            )
        return imports
    

    def __init__(
        self,
        name: str,
        module: Optional[str] = None,
        alias: Optional[str] = None,
        level: Optional[int] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        start_column: Optional[int] = None,
        end_column: Optional[int] = None,
    ):
        super().__init__(
            source=f"{module}.{name}" if module else name,
            alias=alias,
            attributes={
                "name": name,
                "module": module,
                "level": level,
                "start_line": start_line,
                "end_line": end_line,
                "start_column": start_column,
                "end_column": end_column,
            }
        )
        self.name = name
        self.module = module
        self.alias = alias
        self.level = level
        self.start_line = start_line
        self.end_line = end_line
        self.start_column = start_column
        self.end_column = end_column
        
        