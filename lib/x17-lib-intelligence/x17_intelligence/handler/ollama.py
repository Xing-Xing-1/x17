from typing import Any, Dict, List, Optional
from packaging.version import Version, InvalidVersion
import re

from x17_intelligence.handler.base import BaseHandler
from x17_intelligence.exception.ollama import OllamaNotInstalledError

from x17_base.particle.log import LogStream

from x17_base.particle.terminal import Terminal
from x17_base.particle.terminal import Command
from x17_base.particle.terminal import Response

from x17_base.particle.remote import Response as CallResponse
from x17_base.particle.remote import Call
from x17_base.particle.remote import CallSet
from x17_base.particle.remote import Url

from x17_base.particle.platform import Platform



class OllamaHandler(BaseHandler):
    """
    OllamaHandler is a class that handles the Ollama API requests.
    It inherits from the BaseHandler class.

    Usage:
        ollama [flags]
        ollama [command]

    Available Commands:
        serve       Start ollama
        create      Create a model from a Modelfile
        show        Show information for a model
        run         Run a model
        stop        Stop a running model
        pull        Pull a model from a registry
        push        Push a model to a registry
        list        List models
        ps          List running models
        cp          Copy a model
        rm          Remove a model
        help        Help about any command

    """

    def __init__(
        self,
        name: str = None,
        interface: Any = None,
        ollama_host: str = "localhost",
        ollama_port: int = 11434,
        log_stream: Optional[LogStream] = None,
        verbose: bool = True,
    ):
        super().__init__(
            interface=interface,
            name=name,
            log_stream=log_stream,
            verbose=verbose,
        )
        self.platform = Platform(name=self.name)
        self.ollama_host = ollama_host
        self.ollama_port = ollama_port

    def require_env(self) -> Dict[str, str]:
        """
        Check if the environment variables are set.
        """
        is_ollama_installed = self.check_install()
        ollama_path = self.get_exec_path()
        ollama_version = self.check_version()
        is_ollama_host = self.check_host(
            host=self.ollama_host,
            port=self.ollama_port,
        )
        if not is_ollama_host:
            self.start_ollama()
            is_ollama_host = self.check_host(
                host=self.ollama_host,
                port=self.ollama_port,
            )
        
        if all([
            is_ollama_installed,
            bool(ollama_path),
            bool(ollama_version),
            is_ollama_host,
        ]):
            self.log_stream.info(
                "[OK] Ollama environment setup.",
                context="check",
                code=100,
            )
            return {
                "path": ollama_path,
                "version": ollama_version,
                "host": self.check_host(),
            }
        else:
            self.log_stream.error(
                "[FAILED] Ollama environment setup failed.",
                context="check",
                code=110,
            )
            raise OllamaNotInstalledError()
            
    def check_install(self) -> bool:
        result = Terminal.exist_from(program="ollama")
        if result.success:
            self.log_stream.info(
                f"[OK] ollama install checked.",
                context="check",
                code=100,
            )
        else:
            self.log_stream.error(
                "[FAILED] ollama install not found.",
                context="check",
                code=110,
            )
        return result.clean_success

    def get_exec_path(self) -> str:
        result = Terminal.run_from(cmd=Command(cmd="which ollama"))
        if result.success:
            self.log_stream.info(
                f"[OK] ollama executable checked at '{result.stdout}'.",
                context="check",
                code=100,
            )
        else:
            self.log_stream.error(
                "[FAILED] ollama executable not checked.",
                context="check",
                code=110,
            )
        return result.stdout

    def check_version(self) -> str:
        result = Terminal.run_from(cmd=Command(cmd="ollama --version"))
        if result.success:
            match = re.search(r"\b\d+\.\d+(\.\d+)?\b", result.stdout)
            version = match.group(0) if match else ""
            self.log_stream.info(
                f"[OK] ollama version checked '{version}'.", context="check", code=100
            )
        else:
            self.log_stream.error(
                "[FAILED] ollama version not checked.",
                context="check",
                code=110,
            )
        return result.stdout

    def check_host(self, host: str = "localhost", port: int = 11434, retry: int = 3, timeout: int = 5) -> bool:
        url = Url(scheme="http", host=host, port=port)
        response = Call(method="GET", url=url, retry=retry, timeout=timeout).send()
        if response.success:
            self.log_stream.info(message=f"[OK] ollama host checked '{url}'.", context="check", code=100)
        else:
            self.log_stream.error(message=f"[FAILED] ollama host not checked '{url}'.", context="check", code=110)
        return response.success


    # def start_ollama(self) -> bool:
    #     cmd = "ollama serve"
    #     self.log(f"[ACTION] starting ollama", context="start", code=402)
    #     result = Terminal.run_from(Command(cmd=cmd, shell=True), popen=True, wait=5)
    #     if result.success:
    #         self.log(message="[OK] ollama started.", context="start", code=400)
    #         return True
    #     else:
    #         self.log(
    #             message=f"[FAILED] ollama start failed: \n\tstderr: {result.stderr[0:500]}, \n\tstdout: {result.stdout[0:500]}",
    #             level="error",
    #             context="start",
    #             code=411,
    #         )
    #         return False
        
    