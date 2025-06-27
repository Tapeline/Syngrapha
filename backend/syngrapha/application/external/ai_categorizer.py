from abc import abstractmethod
from collections.abc import Collection, Mapping
from typing import Protocol

from syngrapha.domain.product.category import Category
from syngrapha.domain.product.product import ProductId, ProductName


class AICategorizerService(Protocol):
    """Interface for interacting with AI categorizer."""

    @abstractmethod
    async def categorize(
            self, products: Mapping[ProductId, ProductName]
    ) -> Mapping[ProductId, Category]:
        """
        Do the categorizing magic.

        Args:
            products: products to categorize

        Returns: mapping of categories

        """
        raise NotImplementedError
