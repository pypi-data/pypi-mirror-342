import abc


class BaseScrapper(abc.ABC):
    @abc.abstractmethod
    async def start(self, *args, **kwargs) -> None: ...

    async def initialize(self, *args, **kwargs) -> None: ...

    async def close(self, *args, **kwargs) -> None: ...
