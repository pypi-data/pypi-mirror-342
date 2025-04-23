from typing import Protocol


class BaseItem(Protocol):
    @property
    def pipeline_name(self) -> str: ...


class Pipeline(Protocol):
    async def __call__(self, item: BaseItem) -> BaseItem: ...
