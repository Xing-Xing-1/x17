import subprocess
import os

class GUIHandle:
    def __init__(self, app_name: str):
        self.app_name = app_name

    def is_available(self) -> bool:
        return os.path.exists(f"/Applications/{self.app_name}.app")

    def launch(self) -> bool:
        subprocess.run(["open", "-a", self.app_name])
        return True