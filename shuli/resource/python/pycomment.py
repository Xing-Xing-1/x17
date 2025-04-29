# -*- coding: utf-8 -*-
from typing import Optional, List
import ast
import tokenize

from shuli.base.x_comment import Comment
from shuli.base.x_node import NodeType

class PyComment(Comment):
    """
    Python-specific Comment node.
    Supports both `ast-comments` and `tokenize` extraction.
    
    """
    @classmethod
    def from_tokens(
        cls,
        tokens: List[tokenize.TokenInfo],
    ) -> List["PyComment"]:
        results = []
        for token in tokens:
            if token.type == tokenize.COMMENT:
                results.extend(
                    cls.from_token(token)
                )
        return results

    @classmethod
    def from_ast(
        cls,
        node: ast.AST,
    ) -> "PyComment":
        value = getattr(node, "value", "")
        if isinstance(value, str):
            content = value.strip()
        else:
            content = ""
        return [cls(
            content=content,
            start_line=getattr(node, "lineno", None),
            end_line=getattr(node, "end_lineno", None),
            start_column=getattr(node, "col_offset", None),
            end_column=getattr(node, "end_col_offset", None),
            astnode=node,
        )]

    @classmethod
    def from_token(
        cls,
        token: tokenize.TokenInfo,
        inline: bool = False,
    ) -> "PyComment":
        content = token.string.lstrip("# ").rstrip()
        start_line, start_column = token.start
        end_line, end_column = token.end
        return [cls(
            content=content,
            start_line=start_line,
            end_line=end_line,
            start_column=start_column,
            end_column=end_column,
            inline=inline,
        )]

    @classmethod
    def from_code(
        cls,
        code: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        start_column: Optional[int] = None,
        end_column: Optional[int] = None,
        inline: bool = False,
    ) -> "PyComment":
        return [cls(
            content=code.lstrip("# ").rstrip(),
            start_line=start_line,
            end_line=end_line,
            start_column=start_column,
            end_column=end_column,
            inline=inline,
        )]

    def __init__(
        self,
        content: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        start_column: Optional[int] = None,
        end_column: Optional[int] = None,
        inline: bool = False,
        astnode: Optional[ast.AST] = None,
    ):
        super().__init__(
            content=content,
            attributes={
                "start_line": start_line,
                "end_line": end_line,
                "start_column": start_column,
                "end_column": end_column,
                "inline": inline,
            }
        )
        self.start_line = start_line
        self.end_line = end_line
        self.start_column = start_column
        self.end_column = end_column
        self.inline = inline
        self.astnode = astnode
    