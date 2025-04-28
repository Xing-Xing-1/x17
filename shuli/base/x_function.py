# -*- coding: utf-8 -*-
from typing import List, Optional

from shuli.base.x_node import Node
from shuli.base.x_nodetype import NodeType


class Function(Node):
    def __init__(
        self,
        name: str,
        return_type: Optional[str] = None,
        docstring: Optional[str] = None,
        children: Optional[List[Node]] = None,
    ):
        super().__init__(
            type=NodeType.FUNCTION,
            name=name,
            attributes={
                "return_type": return_type,
                "docstring": docstring,
            },
            children=children or [],
        )
