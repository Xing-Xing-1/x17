from abc import ABC, abstractmethod
from typing import Optional
from pangu.particle.platform.app_handle import (
    CLIHandle, GUIHandle, DaemonHandle, ServiceHandle, WebHandle,
)

class BaseLocalApp(ABC):
    """
    抽象本地可控应用程序基类，适配 macOS/Linux/Windows/AWS 等运行环境。
    可组合 CLI / GUI / Daemon / Service / Web 等行为。
    """

    # 基础信息
    name: str                  # e.g., "ollama"
    executable_name: Optional[str] = None  # 默认 CLI 调用名
    app_path: Optional[str] = None         # GUI 或 App 包路径（macOS）
    platform: Optional[str] = None         # e.g., "macos", "linux"

    # 可组合运行能力（五选零～五）
    cli: Optional[CLIHandle] = None
    gui: Optional[GUIHandle] = None
    daemon: Optional[DaemonHandle] = None
    service: Optional[ServiceHandle] = None
    web: Optional[WebHandle] = None

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def is_installed(self) -> bool:
        """检查是否已安装"""
        ...

    def is_available(self) -> bool:
        """任意子能力存在即可视为 available"""
        return any([
            self.cli is not None,
            self.gui is not None,
            self.daemon is not None,
            self.service is not None,
            self.web is not None,
        ])

    def describe(self) -> str:
        """描述该 App 的组成能力"""
        parts = []
        if self.cli: parts.append("CLI")
        if self.gui: parts.append("GUI")
        if self.daemon: parts.append("Daemon")
        if self.service: parts.append("Service")
        if self.web: parts.append("Web")
        return f"{self.name} App [{', '.join(parts)}]"