class ClientException(Exception):
    pass


class HTTPException(ClientException):
    def __init__(self, status_code: int, message: str | None, url: str, method: str) -> None:
        self.status_code = status_code
        self.message = message
        self.url = url
        self.method = method

    def __str__(self) -> str:
        return f"{self.method} {self.url}: {self.status_code}: {self.message}"


class RequestException(ClientException):
    def __init__(self, src: Exception | str, url: str, method: str) -> None:
        self.src = src
        self.url = url
        self.method = method

    def __str__(self) -> str:
        return f"[{self.src.__class__.__name__}]: {self.method} {self.url}: {self.src}"


class PipelineException(Exception): ...
