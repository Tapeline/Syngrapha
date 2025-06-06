from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol

from syngrapha.domain.product.product import ProductId


class AICategorizerService(Protocol):
    """Interface for interacting with AI categorizer."""

    @abstractmethod
    async def notify_need_to_categorize(
            self,
            ids: Collection[ProductId]
    ) -> None:
        """
        Say that AI Cat-r needs to categorize some products.

        Args:
            ids: targets

        """
