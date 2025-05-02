# tests/test_pyargument.py

import ast
import pytest

from shuli.resource.python.pyargument import PyArgument


@pytest.fixture
def full_signature_code():
    return """
def sample(
    a,
    b: int,
    c=1,
    d: str = "hello",
    *args: float,
    e,
    f: bool = True,
    **kwargs: dict,
):
    pass
"""


def test_pyargument_from_ast_arguments_comprehensive(full_signature_code):
    tree = ast.parse(full_signature_code)
    func_node = tree.body[0]
    args = PyArgument.from_ast(func_node.args)

    assert isinstance(args, list)
    assert all(isinstance(arg, PyArgument) for arg in args)
    assert len(args) == 8  # a, b, c, d, args, e, f, kwargs

    # Positional without annotation/default
    assert args[0].name == "a"
    assert args[0].attributes["annotation"] is None
    assert args[0].attributes["default"] is None
    assert args[0].attributes["is_posonly"]

    # Positional with annotation
    assert args[1].name == "b"
    assert args[1].attributes["annotation"] == "int"

    # Positional with default
    assert args[2].name == "c"
    assert args[2].attributes["default"] == "1"

    # Positional with annotation + default
    assert args[3].name == "d"
    assert args[3].attributes["annotation"] == "str"
    assert args[3].attributes["default"] == "'hello'"

    # *args with annotation
    assert args[4].name == "args"
    assert args[4].attributes["is_vararg"]
    assert args[4].attributes["annotation"] == "float"

    # kwonly without default
    assert args[5].name == "e"
    assert args[5].attributes["is_kwonly"]

    # kwonly with default
    assert args[6].name == "f"
    assert args[6].attributes["default"] == "True"
    assert args[6].attributes["annotation"] == "bool"
    assert args[6].attributes["is_kwonly"]

    # **kwargs
    assert args[7].name == "kwargs"
    assert args[7].attributes["is_kwarg"]
    assert args[7].attributes["annotation"] == "dict"