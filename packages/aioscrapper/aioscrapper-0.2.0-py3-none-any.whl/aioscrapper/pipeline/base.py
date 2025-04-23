import abc
from typing import TypeVar, Generic

from ..types import BaseItem

ItemType = TypeVar("ItemType", bound=BaseItem)


class BasePipeline(abc.ABC, Generic[ItemType]):
    @abc.abstractmethod
    async def put_item(self, item: ItemType) -> None: ...

    async def initialize(self) -> None: ...

    async def close(self) -> None: ...
