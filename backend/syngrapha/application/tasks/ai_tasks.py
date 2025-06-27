from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol

from syngrapha.domain.product.product import ProductId


class AICategorizeTaskScheduler(Protocol):
    """Schedule categorizing tasks."""

    @abstractmethod
    async def schedule(self, ids: Collection[ProductId]) -> None:
        """Schedule the task."""
        raise NotImplementedError
