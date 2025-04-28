from shuli.base.x_comment import Comment
from shuli.base.x_nodetype import NodeType


def test_comment_node():
    node = Comment(content="This is a comment.")
    assert node.type == NodeType.COMMENT
    assert node.content == "This is a comment."
