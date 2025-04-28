# -*- coding: utf-8 -*-
from typing import Optional

from shuli.base.x_node import Node
from shuli.base.x_nodetype import NodeType


class Import(Node):
    def __init__(
        self,
        source: str,
        alias: Optional[str] = None,
    ):
        super().__init__(
            type=NodeType.IMPORT,
            name=source,
            attributes={
                "source": source,
                "alias": alias,
            },
        )
