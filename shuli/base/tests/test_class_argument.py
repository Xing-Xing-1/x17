from shuli.base.x_argument import Argument
from shuli.base.x_nodetype import NodeType


def test_argument_node():
    node = Argument(name="x", type_hint="int", default="0")
    assert node.type == NodeType.ARGUMENT
    assert node.name == "x"
    assert node.type_hint == "int"
    assert node.default == "0"
