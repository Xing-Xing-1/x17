# -*- coding: utf-8 -*-
import pytest

from shuli.base.x_node import Node, NodeType


def test_node_creation_leaf_and_composite():
    # Composite nodes
    module_node = Node(type=NodeType.MODULE, name="sample_module")
    class_node = Node(type=NodeType.CLASS, name="SampleClass")
    function_node = Node(type=NodeType.FUNCTION, name="sample_function")

    # Leaf nodes
    import_node = Node(type=NodeType.IMPORT, name="os")
    comment_node = Node(
        type=NodeType.COMMENT, attributes={"content": "this is a comment"}
    )
    codeblock_node = Node(
        type=NodeType.CODEBLOCK, attributes={"content": "print('hello')"}
    )
    argument_node = Node(
        type=NodeType.ARGUMENT, name="arg1", attributes={"type_hint": "str"}
    )

    # Type checking
    assert module_node.type == NodeType.MODULE
    assert class_node.type == NodeType.CLASS
    assert function_node.type == NodeType.FUNCTION
    assert import_node.type == NodeType.IMPORT
    assert comment_node.type == NodeType.COMMENT
    assert codeblock_node.type == NodeType.CODEBLOCK
    assert argument_node.type == NodeType.ARGUMENT


def test_is_composite_and_leaf_properties():
    module_node = Node(type=NodeType.MODULE)
    function_node = Node(type=NodeType.FUNCTION)
    import_node = Node(type=NodeType.IMPORT)

    assert module_node.is_composite is True
    assert function_node.is_composite is True
    assert import_node.is_composite is False

    assert module_node.is_leaf is False
    assert function_node.is_leaf is False
    assert import_node.is_leaf is True


def test_add_child_to_composite():
    parent = Node(type=NodeType.CLASS, name="ParentClass")
    child = Node(type=NodeType.FUNCTION, name="child_function")

    parent.add_child(child)

    assert len(parent.children) == 1
    assert parent.children[0].name == "child_function"


def test_add_child_to_leaf_should_fail():
    leaf = Node(type=NodeType.IMPORT, name="os")
    child = Node(type=NodeType.FUNCTION, name="child_function")

    with pytest.raises(TypeError) as exc_info:
        leaf.add_child(child)

    assert "Cannot add child" in str(exc_info.value)


def test_node_dict_export_for_composite():
    parent = Node(
        type=NodeType.CLASS, name="ParentClass", attributes={"bases": ["BaseClass"]}
    )
    child = Node(
        type=NodeType.FUNCTION,
        name="child_function",
        attributes={"arguments": ["self"]},
    )
    parent.add_child(child)

    exported = parent.dict

    assert exported["type"] == "class"
    assert exported["name"] == "ParentClass"
    assert "children" in exported
    assert len(exported["children"]) == 1
    assert exported["children"][0]["type"] == "function"
    assert exported["children"][0]["name"] == "child_function"


def test_node_dict_export_for_leaf():
    comment = Node(type=NodeType.COMMENT, attributes={"content": "this is a comment"})
    exported = comment.dict

    assert exported["type"] == "comment"
    assert exported["attributes"]["content"] == "this is a comment"
    assert "children" not in exported


def test_node_repr_contains_key_info():
    node = Node(type=NodeType.CLASS, name="SampleClass")
    child = Node(type=NodeType.FUNCTION, name="child_function")
    node.add_child(child)

    representation = repr(node)
    assert "CLASS" not in representation  # 注意大小写，是小写 'class'
    assert "class" in representation.lower()
    assert "SampleClass" in representation
    assert "[1]" in representation or "children=[1]" in representation
