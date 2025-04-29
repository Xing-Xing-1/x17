import ast
from shuli.resource.python.pycodeblock import PyCodeBlock


def test_pycodeblock_init_and_dict():
    cb = PyCodeBlock(
        content="print('Hello')",
        start_line=1,
        end_line=1,
        start_column=0,
        end_column=18
    )
    assert cb.content == "print('Hello')"
    assert cb.start_line == 1
    assert cb.end_line == 1
    assert cb.start_column == 0
    assert cb.end_column == 18
    assert cb.dict["attributes"]["start_line"] == 1
    assert cb.dict["attributes"]["end_column"] == 18
    assert cb.astnode is None


def test_pycodeblock_from_ast_function():
    code = "def greet():\n    print('hi')"
    tree = ast.parse(code)
    func_node = tree.body[0]
    cb = PyCodeBlock.from_ast(func_node)
    assert isinstance(cb, PyCodeBlock)
    assert "def greet" in cb.content
    assert cb.start_line == func_node.lineno
    assert cb.astnode == func_node


def test_pycodeblock_from_ast_expr():
    code = "x = 1"
    tree = ast.parse(code)
    node = tree.body[0]
    cb = PyCodeBlock.from_ast(node)
    assert cb.content.strip() == "x = 1"
    assert cb.start_line == node.lineno
    assert cb.astnode == node


def test_pycodeblock_from_ast_invalid_node():
    # Intentionally pass a partial/invalid node
    class Dummy:
        pass

    dummy_node = Dummy()
    cb = PyCodeBlock.from_ast(dummy_node)
    assert cb.content == ""
    assert cb.astnode == dummy_node