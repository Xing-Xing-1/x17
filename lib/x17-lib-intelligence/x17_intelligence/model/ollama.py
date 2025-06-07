


class OllamaModel:
    def __init__(
        self, 
        name: str,
    ):
        self.name = name
        self.model = None

    def load_model(self):
        # Load the model using the Ollama API
        pass

    def generate(self, prompt: str):
        # Generate text using the loaded model
        pass