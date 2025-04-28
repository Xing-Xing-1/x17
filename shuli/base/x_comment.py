# -*- coding: utf-8 -*-
from typing import Optional

from shuli.base.x_node import Node
from shuli.base.x_nodetype import NodeType


class Comment(Node):
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
            type=NodeType.COMMENT,
            name=None,
            attributes=attributes,
        )
