# -*- coding: utf-8 -*-

import ast
import pytest
from shuli.resource.python.pyimport import PyImport


def test_pyimport_manual_initialization_full():
    imp = PyImport(
        name="os",
        module=None,
        alias=None,
        level=0,
        start_line=1,
        end_line=1,
        start_column=0,
        end_column=10,
    )
    assert imp.source == "os"
    assert imp.alias is None
    assert imp.name == "os"
    assert imp.module is None
    assert imp.level == 0
    assert imp.start_line == 1
    assert imp.end_column == 10
    assert imp.attributes["name"] == "os"
    assert imp.attributes["level"] == 0
    assert imp.dict["type"] == "import"
    assert imp.dict["name"] == "os"


def test_pyimport_from_ast_import():
    code = "import os"
    node = ast.parse(code).body[0]
    imports = PyImport.from_ast(node)
    assert len(imports) == 1
    imp = imports[0]
    assert isinstance(imp, PyImport)
    assert imp.source == "os"
    assert imp.name == "os"
    assert imp.module is None
    assert imp.alias is None


def test_pyimport_from_ast_from_import_single():
    code = "from typing import List"
    node = ast.parse(code).body[0]
    imports = PyImport.from_ast(node)
    assert len(imports) == 1
    imp = imports[0]
    assert imp.source == "typing.List"
    assert imp.name == "List"
    assert imp.module == "typing"
    assert imp.alias is None


def test_pyimport_from_ast_from_import_multiple():
    code = "from typing import List, Dict"
    node = ast.parse(code).body[0]
    imports = PyImport.from_ast(node)
    assert len(imports) == 2
    sources = [imp.source for imp in imports]
    assert "typing.List" in sources
    assert "typing.Dict" in sources


def test_pyimport_dict_export():
    imp = PyImport(
        name="json",
        module="python",
        alias="j",
    )
    d = imp.dict
    assert d["type"] == "import"
    assert d["name"] == "json"
    assert d["attributes"]["alias"] == "j"
    assert d["attributes"]["module"] == "python"


def test_pyimport_repr_format():
    imp = PyImport(
        name="math",
        module=None,
        alias=None,
    )
    out = repr(imp)
    assert out.startswith("PyImport(")
    assert "name=math" in out


def test_pyimport_from_ast_invalid_node_returns_empty():
    node = ast.parse("x = 5").body[0]
    result = PyImport.from_ast(node)
    assert result == []  # Graceful fallback