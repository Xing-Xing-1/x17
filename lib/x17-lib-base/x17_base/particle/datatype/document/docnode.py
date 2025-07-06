from __future__ import annotations
from typing import Union, List, Optional, Dict
from pydantic import BaseModel


class DocNode(BaseModel):
    """
    DocNode 表示结构化文档内容的通用语法树节点。
    type: 节点类型, 如heading,paragraph,list,code
    content: 纯文本内容，或子节点递归结构
    attrs: 附加属性，如 level, language, tag 等
    """

    type: str
    content: Union[str, List[DocNode]]
    attrs: Optional[Dict[str, Union[str, int, bool]]] = {}

    class Config:
        arbitrary_types_allowed = True

