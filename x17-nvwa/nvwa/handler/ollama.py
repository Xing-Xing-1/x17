from typing import Any, Dict, List, Optional, Tuple


from nvwa.handler.base import BaseHandler

from pangu.particle.log import LogStream


class OllamaHandler(BaseHandler):
    """
    OllamaHandler is a class that handles the Ollama API requests.
    It inherits from the BaseHandler class.
    """
    def __init__(
        self, 
        interface: Any,
        name: str = None,
    ):
        super().__init__(
            interface=interface,
            name=f"{name or self.__class__.__name__}",
        )
        