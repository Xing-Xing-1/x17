# -*- coding: utf-8 -*-
import ast
import tokenize
import io

from shuli.resource.python.pycomment import PyComment

def test_pycomment_init_basic():
    comment = PyComment(
        content="This is a comment",
        start_line=5,
        end_line=5,
        start_column=0,
        end_column=20,
        inline=False,
    )
    assert comment.content == "This is a comment"
    assert comment.start_line == 5
    assert comment.end_line == 5
    assert comment.inline is False
    assert comment.dict["attributes"]["inline"] is False


def test_pycomment_from_code():
    raw_comment = "# Code comment example"
    result = PyComment.from_code(
        code=raw_comment,
        start_line=10,
        end_line=10,
        start_column=2,
        end_column=25,
        inline=True,
    )
    assert isinstance(result, list)
    assert isinstance(result[0], PyComment)
    assert result[0].content == "Code comment example"
    assert result[0].inline is True


def test_pycomment_from_token():
    code = "x = 42  # inline comment\n# standalone comment\n"
    tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))

    inline_token = next(t for t in tokens if "# inline" in t.string)
    standalone_token = next(t for t in tokens if "# standalone" in t.string)

    inline_result = PyComment.from_token(inline_token, inline=True)
    assert isinstance(inline_result, list)
    assert isinstance(inline_result[0], PyComment)
    assert "inline comment" in inline_result[0].content
    assert inline_result[0].inline is True

    standalone_result = PyComment.from_token(standalone_token)
    assert isinstance(standalone_result, list)
    assert isinstance(standalone_result[0], PyComment)
    assert "standalone comment" in standalone_result[0].content
    assert standalone_result[0].inline is False


def test_pycomment_from_ast_with_ast_comments():
    try:
        import ast_comments
    except ImportError:
        import pytest
        pytest.skip("ast_comments not installed")

    code = "# top level comment\nx = 1  # trailing comment\n"
    tree = ast_comments.parse(code)
    comments = []
    for node in tree.body:
        comments.extend(PyComment.from_ast(node))
    assert isinstance(comments, list)
    assert all(isinstance(c, PyComment) for c in comments)
    assert any("top level" in c.content for c in comments) or any("trailing" in c.content for c in comments)
    
def test_pycomment_from_tokens_batch():
    code = """
# Module-level comment
x = 1  # Inline comment
# Another comment
"""
    tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
    comments = PyComment.from_tokens(tokens)

    assert isinstance(comments, list)
    assert len(comments) == 3

    contents = [c.content for c in comments]
    assert "Module-level comment" in contents
    assert "Inline comment" in contents
    assert "Another comment" in contents
    