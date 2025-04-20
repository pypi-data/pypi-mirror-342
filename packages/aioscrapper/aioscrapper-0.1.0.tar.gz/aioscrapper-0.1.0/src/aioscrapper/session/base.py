import abc

from ..types import Request, Response


class BaseSession(abc.ABC):
    def __init__(self, timeout: float | None = None, ssl: bool | None = None) -> None:
        self._timeout = timeout
        self._ssl = ssl

    @abc.abstractmethod
    async def make_request(self, request: Request) -> Response: ...

    async def close(self) -> None: ...
