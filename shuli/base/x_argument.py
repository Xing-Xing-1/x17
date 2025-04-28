# -*- coding: utf-8 -*-
from typing import Optional

from shuli.base.x_node import Node
from shuli.base.x_nodetype import NodeType


class Argument(Node):
    def __init__(
        self,
        name: str,
        type_hint: Optional[str] = None,
        default: Optional[str] = None,
        attributes: Optional[dict] = None,
    ):
        attributes = attributes or {}
        attributes.update({
            "type_hint": type_hint,
            "default": default,
        })
        super().__init__(
            type=NodeType.ARGUMENT,
            name=name,
            attributes=attributes,
        )
