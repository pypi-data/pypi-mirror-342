from typing import Protocol

from .session import Request, RequestParams, Response


class RequestMiddleware(Protocol):
    async def __call__(self, request: Request, params: RequestParams) -> None: ...


class ResponseMiddleware(Protocol):
    async def __call__(self, params: RequestParams, response: Response) -> None: ...
