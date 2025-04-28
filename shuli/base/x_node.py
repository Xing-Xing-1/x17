# -*- coding: utf-8 -*-
from enum import Enum
from typing import Any, Dict, List, Optional

from shuli.base.x_nodetype import NodeType


class Node:
    """
    A generic Node that represents any code structure element.
    In Node Tree, each Node can be either a composite or a leaf node.
    Composite Node can have children (e.g., MODULE, CLASS, FUNCTION)
    Leaf Node cannot have children (e.g., IMPORT, COMMENT, CODEBLOCK, ARGUMENT)
    Node can loop through its children and export itself as a dictionary.

    """

    def __init__(
        self,
        type: NodeType,
        name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        children: Optional[List["Node"]] = None,
    ):
        self.type = type
        self.name = name
        self.children = []
        self.attributes = attributes or {}
        for key, value in self.attributes.items():
            setattr(self, key, value)

        if self.is_composite:
            self.children = children or []
        elif children:
            raise ValueError(f"Node of type '{self.type.value}' cannot have children.")

    # --- Properties ---

    @property
    def is_composite(self) -> bool:
        return self.type in {
            NodeType.MODULE,
            NodeType.CLASS,
            NodeType.FUNCTION,
        }

    @property
    def is_leaf(self) -> bool:
        return not self.is_composite

    # --- Methods ---

    def add_child(
        self,
        child: "Node",
    ) -> None:
        if not self.is_composite:
            raise TypeError(f"Cannot add child to Leaf Node '{self.type.value}'")
        self.children.append(child)

    @property
    def dict(self) -> Dict[str, Any]:
        result = {
            "type": self.type.value,
            "name": self.name,
            "attributes": self.attributes,
        }
        if self.is_composite:
            result["children"] = [child.dict for child in self.children]
        return result

    def __repr__(self) -> str:
        attributes = []
        for key, value in self.dict.items():
            if isinstance(value, list):
                value = f"[{len(value)}]"
            if value:
                attributes.append(f"{key}={value}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"
