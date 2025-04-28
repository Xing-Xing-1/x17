from shuli.base.x_class import Class
from shuli.base.x_nodetype import NodeType


def test_class_node():
    node = Class(name="MyClass", bases=["BaseClass"], docstring="A class example")
    assert node.type == NodeType.CLASS
    assert node.name == "MyClass"
    assert node.bases == ["BaseClass"]
    assert node.docstring == "A class example"
