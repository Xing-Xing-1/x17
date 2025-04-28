# -*- coding: utf-8 -*-

import ast
import pytest

from shuli.resource.python.pyimport import PyImport

def test_pyimport_manual_initialization():
    imp = PyImport(
        name="os",
        module=None,
        alias=None,
        level=None,
        start_line=1,
        end_line=1,
        start_column=0,
        end_column=10,
    )
    assert imp.source == "os"
    assert imp.alias is None
    assert imp.name == "os"
    assert imp.module is None
    assert imp.start_line == 1
    assert imp.attributes["name"] == "os"
    assert imp.attributes["start_line"] == 1
    assert imp.dict["type"] == "import"
    assert imp.dict["name"] == "os"

def test_pyimport_from_ast_import():
    code = "import os"
    node = ast.parse(code).body[0]
    imports = PyImport.from_ast(node)
    assert len(imports) == 1
    imp = imports[0]
    assert imp.source == "os"
    assert imp.alias is None
    assert imp.module is None

def test_pyimport_from_ast_from_import_single():
    code = "from typing import List"
    node = ast.parse(code).body[0]
    imports = PyImport.from_ast(node)
    assert len(imports) == 1
    imp = imports[0]
    assert imp.source == "typing.List"
    assert imp.module == "typing"
    assert imp.name == "List"

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
        name="os",
        module=None,
        alias=None,
    )
    exported = imp.dict
    assert exported["type"] == "import"
    assert exported["name"] == "os"

def test_pyimport_repr():
    imp = PyImport(
        name="os",
        module=None,
        alias=None,
    )
    output = repr(imp)
    assert "PyImport" in output
    assert "name=os" in output

def test_pyimport_from_ast_invalid_node():
    code = "print('hello')"
    node = ast.parse(code).body[0]
    result = PyImport.from_ast(node)
    assert result == []
    