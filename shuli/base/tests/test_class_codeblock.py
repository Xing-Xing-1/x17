from shuli.base.x_codeblock import CodeBlock
from shuli.base.x_nodetype import NodeType


def test_codeblock_node():
    node = CodeBlock(content="print('hello')")
    assert node.type == NodeType.CODEBLOCK
    assert node.content == "print('hello')"
