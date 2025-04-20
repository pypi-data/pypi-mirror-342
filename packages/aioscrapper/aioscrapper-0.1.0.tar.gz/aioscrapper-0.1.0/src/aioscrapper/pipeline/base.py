import abc
from typing import TypeVar, Generic, Protocol


class BaseItem(Protocol):
    @property
    def pipeline_name(self) -> str: ...


ItemType = TypeVar("ItemType", bound=BaseItem)


class BasePipeline(abc.ABC, Generic[ItemType]):
    @abc.abstractmethod
    async def put_item(self, item: ItemType) -> None: ...

    async def initialize(self) -> None: ...

    async def close(self) -> None: ...
