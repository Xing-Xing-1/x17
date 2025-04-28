# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, Any
import ast
import tokenize
import io

from shuli.resource.python.pyimport import Import
from shuli.resource.python.pycomment import Comment
from shuli.resource.python.pyclass import Class
from shuli.resource.python.pyfunction import Function
from shuli.resource.python.pycodeblock import CodeBlock
from shuli.resource.python.pyargument import Argument


class Python:
    
    def __init__(
        self, 
        name: str,
        code: str,
    ):
        self.name = name
        self.code = code
        self.tree = ast.parse(code)
        self.classes: List[Class] = []
        self.functions: List[Function] = []
        self.imports: List[Import] = []
        self.comments: List[Comment] = []

    def parse(self) -> Dict[str, Any]:
        for node in self.tree.body:
            if isinstance(node, ast.ClassDef):
                self.classes.append(
                    self._parse_class(node),
                )
            elif isinstance(node, ast.FunctionDef):
                self.functions.append(
                    self._parse_function(node),
                )
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                self.imports.extend(
                    self._parse_import(node),
                )
        
        tokens = tokenize.generate_tokens(io.StringIO(self.code).readline)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                self.comments.append(
                    Comment(
                        content=token.string.strip("# ").strip()
                    )
                )
        
        return self.dict

    def _parse_class(
        self,
        node: ast.ClassDef,
    ) -> Class:
        methods = []
        attributes = []

        for elem in node.body:
            if isinstance(elem, ast.FunctionDef):
                methods.append(self._parse_function(elem))
            elif isinstance(elem, ast.Assign):
                # 尝试拿简单的属性赋值（如 self.name = xxx）
                for target in elem.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)

        return Class(
            name=node.name,
            bases=[base.id for base in node.bases if isinstance(base, ast.Name)],
            attributes=attributes,
            methods=methods,
            docstring=ast.get_docstring(node),
            body=CodeBlock(),  # 暂时不给原始代码块
        )

    def _parse_function(
        self,
        node: ast.FunctionDef,
    ) -> Function:
        arguments = []
        for arg in node.args.args:
            arguments.append(Argument(name=arg.arg))
        
        return Function(
            name=node.name,
            arguments=arguments,
            return_type=None,  # 暂不提取 return 类型
            docstring=ast.get_docstring(node),
            body=CodeBlock()
        )
        
    def _parse_import(
        self,
        node: ast.AST,
    ) -> List[Import]:  # 注意：返回List而不是单个Import
        imports = []

        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    Import(
                        source=alias.name,
                        alias=alias.asname,
                    )
                )
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                full_source = f"{node.module}.{alias.name}" if node.module else alias.name
                imports.append(
                    Import(
                        source=full_source,
                        alias=alias.asname,
                    )
                )
        return imports

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "classes": [cls.dict for cls in self.classes],
            "functions": [func.dict for func in self.functions],
            "imports": [imp.dict for imp in self.imports],
            "comments": [com.dict for com in self.comments],
        }

        
