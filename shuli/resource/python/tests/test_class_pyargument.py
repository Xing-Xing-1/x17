# tests/test_pyargument_astnode.py
import ast
from shuli.resource.python.pyargument import PyArgument

def test_pyargument_init_with_astnode():
    node = ast.parse("def func(x: int = 10): pass").body[0].args.args[0]
    arg = PyArgument(
        name="x",
        type_hint="int",
        default="10",
        is_vararg=False,
        is_kwarg=False,
        is_kwonly=False,
        start_line=1,
        end_line=1,
        start_column=0,
        end_column=10,
        astnode=node,
    )
    assert arg.name == "x"
    assert arg.astnode == node
    assert isinstance(arg.astnode, ast.arg)

def test_pyargument_from_ast_arg_includes_astnode():
    code = "def func(x: int = 10): pass"
    tree = ast.parse(code)
    func_node = tree.body[0]
    x_arg = func_node.args.args[0]
    parsed_args = PyArgument.from_ast_arg(x_arg, default="10")
    assert len(parsed_args) == 1
    arg = parsed_args[0]
    assert arg.name == "x"
    assert arg.type_hint == "int"
    assert arg.default == "10"
    assert isinstance(arg.astnode, ast.arg)

def test_pyargument_from_ast_arguments_all_astnode_preserved():
    code = """
def func(a, b=2, *args, c, d=4, **kwargs): pass
"""
    tree = ast.parse(code)
    func_node = tree.body[0]
    args = PyArgument.from_ast_arguments(func_node.args)
    assert all(isinstance(arg.astnode, ast.arg) for arg in args)