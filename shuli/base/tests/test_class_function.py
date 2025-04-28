from shuli.base.x_function import Function
from shuli.base.x_nodetype import NodeType


def test_function_node():
    node = Function(name="greet", return_type="str", docstring="Greet function")
    assert node.type == NodeType.FUNCTION
    assert node.name == "greet"
    assert node.return_type == "str"
    assert node.docstring == "Greet function"
