# test_pynode.py
import ast
from typing import Any, Dict
from shuli.resource.python.pynode import PyNode
from shuli.base.nodetype import NodeType

SAMPLE_CODE = '''
import os
from typing import List

class MyClass:
    def __init__(self, x: int):
        self.x = x

    def method(self):
        if self.x > 0:
            print("Positive")
        else:
            print("Non-positive")

def top_level_function():
    for i in range(3):
        print(i)
'''

def test_pynode_basic_structure():
    tree = ast.parse(SAMPLE_CODE)
    nodes = PyNode.from_ast(tree, type=NodeType.MODULE)
    for node in nodes:
        assert isinstance(node, PyNode)
        assert node.type == NodeType.MODULE
        assert node.astnode.__class__.__name__ == "Module"
        child_types = [child.astnode.__class__.__name__ for child in node.children]
        assert "Import" in child_types
        assert "ImportFrom" in child_types
        assert "ClassDef" in child_types
        assert "FunctionDef" in child_types

def test_pynode_recursively_builds_tree():
    roots = PyNode.from_ast(ast.parse(SAMPLE_CODE), type=NodeType.MODULE)
    for root in roots:
        class_node = next(c for c in root.children if isinstance(c.astnode, ast.ClassDef))
        method_node = next(c for c in class_node.children if getattr(c, "name", None) == "method")
        if_node = next(c for c in method_node.children if isinstance(c.astnode, ast.If))
        assert isinstance(if_node.astnode, ast.If)
        assert if_node.parent == method_node
        assert method_node.parent == class_node

def test_pynode_export_dict_structure():
    roots = PyNode.from_ast(ast.parse(SAMPLE_CODE), type=NodeType.MODULE)
    for root in roots:
        result: Dict[str, Any] = root.export()
        assert isinstance(result, dict)
        assert "type" in result
        assert "name" in result
        assert "attributes" in result
        assert "children" in result
        assert any(c["attributes"]["asttype"] == "ClassDef" for c in result["children"])

def test_pynode_code_property():
    roots = PyNode.from_ast(ast.parse("x = 1"), type=NodeType.MODULE)
    for root in roots:
        assert isinstance(root.code, str)
        assert "x = 1" in root.code

def test_pynode_handles_missing_attributes_gracefully():
    node = ast.Pass()
    pynodes = PyNode.from_ast(node, type=NodeType.CODEBLOCK)
    for pynode in pynodes:
        assert pynode.attributes.get("start_line") is None
        assert pynode.attributes["asttype"] == "Pass"

def test_pynode_parent_relationships():
    code = "def func():\n    x = 1"
    roots = PyNode.from_ast(ast.parse(code))
    for root in roots:
        func = root.children[0]
        assign = func.children[0]
        assert assign.parent == func
        assert func.parent == root