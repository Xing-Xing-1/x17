from shuli.base.x_import import Import
from shuli.base.x_nodetype import NodeType


def test_import_node():
    node = Import(source="os", alias="os_alias")
    assert node.type == NodeType.IMPORT
    assert node.name == "os"
    assert node.source == "os"
    assert node.alias == "os_alias"
