# -*- coding: utf-8 -*-
from shuli.base.x_node import Node
from shuli.base.x_nodetype import NodeType


class Comment(Node):
    def __init__(self, content: str):
        super().__init__(
            type=NodeType.COMMENT,
            name=None,
            attributes={
                "content": content,
            },
        )
