# pangu/particle/platform/env.py

import os
import sys
import platform
import socket
from typing import Dict


class Platform:
    """
    Lightweight environment model for physical/local platforms.
    Supports detection of OS type, architecture, docker status, and runtime traits.
    
    """

    def __init__(
        self, 
        name: str = None, 
        **kwargs,
    ):
        self.name = name or f"{self.__class__.__name__}"
        self.platform = sys.platform
        self.os = platform.system().lower()  # e.g. darwin, linux, windows
        self.architecture = platform.machine()  # e.g. arm64, x86_64
        self.python_version = platform.python_version()
        self.hostname = socket.gethostname()
        self.env_vars=dict(os.environ)
        self.is_docker = self.check_docker()
        self.plugins = kwargs.get("plugins", {})
        
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)
        
    @property
    def ip_address(self) -> str:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"
    
    
    def check_docker(self) -> bool:
        try:
            with open("/proc/1/cgroup", "rt") as f:
                return "docker" in f.read() or "kubepods" in f.read()
        except Exception:
            return False

    @property
    def is_macos(self) -> bool:
        return self.os == "darwin"

    @property
    def is_linux(self) -> bool:
        return self.os == "linux"

    @property
    def is_windows(self) -> bool:
        return self.os == "windows"

    @property
    def is_local(self) -> bool:
        return not self.is_docker  # Cloud check could be added later
