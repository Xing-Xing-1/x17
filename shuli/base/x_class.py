# -*- coding: utf-8 -*-
from typing import List, Optional

from shuli.base.x_node import Node
from shuli.base.x_nodetype import NodeType


class Class(Node):
    def __init__(
        self,
        name: str,
        bases: Optional[List[str]] = None,
        docstring: Optional[str] = None,
        attributes: Optional[dict] = None,
        children: Optional[List[Node]] = None,
    ):
        attributes = attributes or {}
        attributes.update({
            "bases": bases or [],
            "docstring": docstring,
        })
        super().__init__(
            type=NodeType.CLASS,
            name=name,
            attributes=attributes,
            children=children or [],
        )
