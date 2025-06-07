

from x17_intelligence.interface.base import BaseInterface
from x17_intelligence.interface.ollama import OllamaModel
from x17_intelligence.handler.ollama import OllamaHandler

from x17_base.particle.log import LogGroup
from x17_base.particle.log import LogStream


class OllamaInterface(BaseInterface):
    def __init__(
        self, 
        name: str,
    ):
        super().__init__()
        self.log_group = LogGroup(name=f"ollama")
        self.models = {}
        # self.log_group = LogGroup("ollama")
        # self.log_stream = LogStream("ollama_stream")
        # self.log_core.register_group(self.log_group)
    
        self.handler = OllamaHandler(
            
        )
        self.log = log_stream(name=f"Handler[{interface.model_name}]")
        self.log.attach_to(interface.log)  # Attach to interface's log group
