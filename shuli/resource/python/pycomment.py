# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, Any

from shuli.base.x_comment import Comment

class PyComment(Comment):
    def __init__(
        self,
        content: str,
    ):
        super().__init__(content=content)
        
    