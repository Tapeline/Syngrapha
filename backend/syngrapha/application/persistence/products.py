from abc import abstractmethod
from collections.abc import Collection, Mapping
from typing import Protocol

from syngrapha.domain.product.category import Category
from syngrapha.domain.product.product import ProductId, ProductName


class ProductGateway(Protocol):
    """Access to product store (ensures consistency)."""

    @abstractmethod
    async def get_product_names(
            self, ids: Collection[ProductId]
    ) -> Mapping[ProductId, ProductName]:
        """
        Get product names.

        Args:
            ids: ids of products to get

        Returns: mapping of id -> name

        """
        raise NotImplementedError

    @abstractmethod
    async def save_product_categories(
            self,
            categories: Mapping[ProductId, Category | None]
    ) -> None:
        """
        Get all transactions owned by the given user.

        Args:
            categories: category mapping to set

        """
        raise NotImplementedError
