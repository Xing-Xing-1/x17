from typing import Optional, Dict, Any, Union, List
import json

from x17_base.particle.datestamp.datestamp import Datestamp
from x17_base.particle.log.log_event import LogEvent
from x17_base.particle.remote.url import Url

class Response:
    """
    Represents an HTTP response.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Response":
        return cls(
            code=data.get("code", None),
            status=data.get("status", 0),
            headers=data.get("headers", {}),
            body=data.get("body", b""),
            url=data.get("url", ""),
            stdout=data.get("stdout", ""),
            error=data.get("error", ""),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "Response":
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __init__(
        self,
        code: Optional[int] = None,
        status: Optional[int] = None,
        headers: dict = {},
        body: bytes = b"",
        url: str = "",
        stdout: str = "",
        error: str = "",
    ):
        self.code = code or status or 0
        self.status = code or status or 0
        self.headers = headers
        self.body = body
        self.url = Url(url) if not isinstance(url, Url) else url
        self.stdout = stdout
        self.error = error

    @property
    def attr(self) -> List[str]:
        return [
            "code",
            "status",
            "headers",
            "body",
            "url",
            "stdout",
            "error",
        ]

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "status": self.status,
            "headers": self.headers,
            "body": self.body,
            "url": self.url,
            "stdout": self.stdout,
            "error": self.error,
        }

    @property
    def success(self) -> bool:
        return 200 <= self.status < 300

    @property
    def encoding(self) -> str:
        content_type = self.headers.get("Content-Type", "")
        if "charset=" in content_type:
            return content_type.split("charset=")[-1].strip()
        return "utf-8"

    @property
    def text(self) -> str:
        return self.body.decode(self.encoding, errors="replace")

    @property
    def log(self) -> LogEvent:
        return [
            LogEvent(
                message=self.text,
                name=self.__class__.__name__,
                level="INFO" if self.success else "ERROR",
                datestamp=Datestamp.now().datestamp_str,
                status=self.status,
                body=self.body.decode(self.encoding, errors="replace"),
                url=str(self.url),
                error=self.error,
            )
        ]

    def __repr__(self):
        attr_parts = []
        for key in self.attr:
            value = getattr(self, key, None)
            if value:
                attr_parts.append(f"{key}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(attr_parts)})"

    def __str__(self):
        return self.__repr__()

    def json(self, check=True) -> Union[Dict[str, Any], Any]:
        try:
            return json.loads(self.text)
        except Exception as e:
            if check:
                raise e
            return {}

    def export(
        self,
    ) -> Dict[str, Any]:
        return self.dict

    