# -*- coding: utf-8 -*-
from typing import Optional

from shuli.base.x_node import Node
from shuli.base.x_nodetype import NodeType


class CodeBlock(Node):
    def __init__(
        self,
        content: str,
        attributes: Optional[dict] = None,
    ):
        attributes = attributes or {}
        attributes.update({
            "content": content,
        })
        super().__init__(
            type=NodeType.CODEBLOCK,
            name=None,
            attributes=attributes,
        )
