# -*- coding: utf-8 -*-

class OllamaNotInstalledError(Exception):
    def __init__(
        self, 
        hint: str = None,
    ):
        message = (
            "Ollama is not installed or not found in system PATH.\n"
            "Please install it manually or switch to API based platform:\n"
            "- For Linux: curl -fsSL https://ollama.com/install.sh | sh\n"
            "- For Macos: brew install ollama/tap/ollama\n",
            "Hint: {hint}\n",
        )
        super().__init__(message)
        
class OllamaInvokeError(Exception):
    def __init__(
        self, 
        hint: str = None,
    ):
        message = (
            "Ollama invoke failed.\n"
            "Please check related logs and try again.\n"
            "Hint: {hint}\n",
        )
        super().__init__(message)