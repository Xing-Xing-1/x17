from typing import Optional, Dict, Any, Union

from pangu.particle.remote.call import Call
from pangu.particle.remote.url import Url
from pangu.particle.remote.response import Response


class WebHandle:
    def __init__(
        self,
        url: Union[str, Url] = None,
        scheme: str = "https",
        host: str = "",
        port: Optional[int] = None,
        path: str = "",
        query: Optional[Dict[str, Any]] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.url = Url(
            url=url,
            scheme=scheme,
            host=host,
            port=port,
            path=path,
            query=query,
            user=user,
            password=password,
        )

    def is_available(
        self,
        retry: int = 3,
        timeout: int = 3,
    ) -> bool:
        call = Call(
            method="GET",
            url=self.url,
            retry=retry,
            timeout=timeout,
        )
        resp = call.send()
        return resp.success

    def __str__(self) -> str:
        return str(self.url)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(url={self.url})"

    @property
    def dict(self) -> Dict[str, Any]:
        return self.url.dict

    def get(
        self,
        path: str = "",
        query: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        retry: int = 3,
        timeout: int = 3,
    ) -> Response:
        url = self.url.join_path(path).join_querys(query)
        call = Call(
            method="GET",
            url=url,
            headers=headers,
            retry=retry,
            timeout=timeout,
        )
        response = call.send()
        return response

    def post(
        self,
        path: str = "",
        query: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Union[str, bytes, Dict]] = None,
        retry: int = 3,
        timeout: int = 3,
    ) -> Response:
        url = self.url.join_path(path).join_querys(query)
        call = Call(
            method="POST",
            url=url,
            headers=headers,
            body=body,
            retry=retry,
            timeout=timeout,
        )
        response = call.send()
        return response
