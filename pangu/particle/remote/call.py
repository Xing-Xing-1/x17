import urllib.request
import urllib.parse
import json
from typing import Optional, Dict, Any, Union
from pangu.particle.remote.url import Url
from pangu.particle.remote.response import Response


class Call:
    def __init__(
        self,
        method: str,
        url: Union[str, Url],
        headers: Optional[Dict[str, str]] = None,
        query: Optional[Dict[str, Any]] = None,
        body: Optional[Union[str, bytes, dict]] = None,
        timeout: int = 10,
    ):
        self.method = method.upper()
        self.url = Url(url=url) if isinstance(url, str) else url
        self.headers = headers or {}
        self.query = query or {}
        self.body = body
        self.timeout = timeout

    def send(self) -> Response:
        full_url = self.url.with_query({**self.url.query, **self.query})
        data = None

        if isinstance(self.body, dict):
            data = json.dumps(self.body).encode("utf-8")
            self.headers.setdefault("Content-Type", "application/json")
        elif isinstance(self.body, str):
            data = self.body.encode("utf-8")
        elif isinstance(self.body, bytes):
            data = self.body

        req = urllib.request.Request(
            url=full_url.link,
            data=data,
            headers=self.headers,
            method=self.method,
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                response_body = res.read()
                return Response(
                    status=res.status,
                    headers=dict(res.getheaders()),
                    body=response_body,
                    url=full_url,
                )
        except urllib.error.HTTPError as e:
            return Response(
                status=e.code,
                headers=dict(e.headers),
                body=e.read(),
                url=full_url,
                error=str(e),
            )
        except Exception as e:
            return Response(
                status=0,
                headers={},
                body=b"",
                url=full_url,
                error=str(e),
            )
