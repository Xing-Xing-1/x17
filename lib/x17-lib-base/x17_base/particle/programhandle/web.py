from typing import Optional, Dict, Any, Union

from x17_base.particle.remote.call import Call
from x17_base.particle.remote.url import Url
from x17_base.particle.remote.response import Response
from x17_base.particle.duration import Duration


class WebHandle:
    
    @classmethod
    def from_name(
        cls,
        name: str,
        url: Union[str, Url],
        registries: Optional[Dict[str, Call]] = None,
    ) -> "WebHandle":
        if isinstance(url, str):
            url = Url.from_str(url)
        return cls(
            name=name,
            url=url,
            registries=registries or {},
        )
    
    def __init__(
        self,
        name: str,
        url: Url,
        registries: Optional[Dict[str, Call]] = None,
    ):
        self.name = name
        self.url = url
        self.scheme = self.url.scheme
        self.host = self.url.host
        self.port = self.url.port
        self.path = self.url.path
        self.query = self.url.query
        self.registries = registries or {}
    
    @property
    def is_available(self) -> bool:
        call = Call(
            method="GET",
            url=self.url,
            retry=3,
            timeout=3,
        )
        resp = call.send()
        return resp.success

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "url": str(self.url),
            "is_available": self.is_available,
        }

    def __str__(self) -> str:
        return str(self.url)
    
    def __bool__(self) -> bool:
        return self.is_available

    def __len__(self) -> int:
        return 1 if self.is_available else 0

    def __repr__(self) -> str:
        attributes = []
        for unit, value in self.dict.items():
            if value:
                attributes.append(f"{unit}={value}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def run(
        self,
        call: Call,
    ) -> Response:
        response = call.send()
        return response

    def get(
        self,
        path: Optional[Union[str, Url]] = None,
        headers: Optional[Dict[str, str]] = None,
        query: Optional[Dict[str, Any]] = None,
        body: Optional[Union[str, bytes, Dict]] = None,
        timeout: int = 10,
        retry: int = 1,
        interval: Duration = None,
    ) -> Response:
        url = self.url.join_path(path)
        call = Call(
            method="GET",
            url=url,
            headers=headers,
            query=query,
            body=body,
            timeout=timeout,
            retry=retry,
            interval=interval,
        )
        return self.run(call=call)

    def post(
        self,
        path: Optional[Union[str, Url]] = None,
        headers: Optional[Dict[str, str]] = None,
        query: Optional[Dict[str, Any]] = None,
        body: Optional[Union[str, bytes, Dict]] = None,
        timeout: int = 10,
        retry: int = 1,
        interval: Duration = None,
    ) -> Response:
        url = self.url.join_path(path)
        call = Call(
            method="POST",
            url=url,
            headers=headers,
            query=query,
            body=body,
            timeout=timeout,
            retry=retry,
            interval=interval,
        )
        return self.run(call=call)

    def get_version(self, **kwargs: Any) -> Optional[str]:
        return "Not supported"
    
    def register(
        self,
        label: str,
        call: Call,
        as_method: bool = False,
    ) -> None:
        if label in self.registries:
            raise ValueError(f"Label '{label}' is already registered.")
        self.registries[label] = call
        
        if as_method:
            def _run_call(_call=call, **kwargs):
                return self.run(_call)
            setattr(self, label, _run_call)
    
    def get_registered(
        self,
        label: str,
    ) -> Optional[Call]:
        return self.registries.get(label, None)
    
    