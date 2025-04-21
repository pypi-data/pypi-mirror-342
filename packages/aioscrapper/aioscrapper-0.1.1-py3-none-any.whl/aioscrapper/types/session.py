import json
from dataclasses import dataclass
from typing import Union, Mapping, Any, Callable, Awaitable, TypedDict, Protocol
from urllib.parse import urlencode

QueryParams = Mapping[str, Union[str, int, float]]

Cookies = Mapping[str, str]
Headers = Mapping[str, str]


class BasicAuth(TypedDict):
    username: str
    password: str


@dataclass(slots=True)
class Request:
    url: str
    method: str
    params: QueryParams | None = None
    data: Any = None
    json_data: Any = None
    cookies: Cookies | None = None
    headers: Headers | None = None
    auth: BasicAuth | None = None
    proxy: str | None = None
    timeout: float | None = None

    @property
    def full_url(self) -> str:
        return f"{self.url}{urlencode(self.params or {})}"


@dataclass(slots=True)
class RequestParams:
    callback: Callable[..., Awaitable] | None = None
    cb_kwargs: dict[str, Any] | None = None
    errback: Callable[..., Awaitable] | None = None


class RequestSender(Protocol):
    async def __call__(
        self,
        url: str,
        method: str = "GET",
        callback: Callable[..., Awaitable] | None = None,
        cb_kwargs: dict[str, Any] | None = None,
        errback: Callable[..., Awaitable] | None = None,
        params: QueryParams | None = None,
        data: Any = None,
        json_data: Any = None,
        cookies: Cookies | None = None,
        headers: Headers | None = None,
        proxy: str | None = None,
        auth: BasicAuth | None = None,
        timeout: float | None = None,
        priority: int = 0,
    ) -> None: ...


class Response:
    def __init__(
        self,
        url: str,
        method: str,
        params: QueryParams | None,
        status: int,
        headers: Headers,
        cookies: Cookies,
        content: bytes,
        content_type: str | None,
    ) -> None:
        self._url = url
        self._method = method
        self._params = params
        self._status = status
        self._headers = headers
        self._cookies = cookies
        self._content = content
        self._content_type = content_type

    @property
    def url(self) -> str:
        return self._url

    @property
    def method(self) -> str:
        return self._method

    @property
    def params(self) -> QueryParams | None:
        return self._params

    @property
    def status(self) -> int:
        return self._status

    @property
    def headers(self) -> Headers | None:
        return self._headers

    @property
    def cookies(self) -> Cookies | None:
        return self._cookies

    @property
    def content_type(self) -> str | None:
        return self._content_type

    def bytes(self) -> bytes:
        return self._content

    def json(self) -> Any:
        return json.loads(self._content) if self._content is not None else None

    def text(self, encoding: str = "utf-8") -> str | None:
        return self._content.decode(encoding) if self._content is not None else None
