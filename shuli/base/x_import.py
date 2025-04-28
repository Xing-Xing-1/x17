# -*- coding: utf-8 -*-
from typing import Optional

from shuli.base.x_node import Node
from shuli.base.x_nodetype import NodeType


class Import(Node):
    def __init__(
        self,
        source: str,
        alias: Optional[str] = None,
        attributes: Optional[dict] = None,
    ):
        attributes = attributes or {}
        attributes.update({
            "source": source,
            "alias": alias,
        })
        super().__init__(
            type=NodeType.IMPORT,
            name=source,
            attributes = attributes,
        )
