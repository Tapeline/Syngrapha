from abc import abstractmethod
from collections.abc import Collection, Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from syngrapha.domain.product.category import Category
from syngrapha.domain.transaction.transaction import Transaction, TransactionId
from syngrapha.domain.product.product import ProductId, ProductName
from syngrapha.domain.user import UserId


class ProductGateway(Protocol):
    """Access to product store."""

    @abstractmethod
    async def get_product_names(
            self, ids: Collection[ProductId]
    ) -> Mapping[ProductId, ProductName]:
        """
        Get product names.

        Args:
            ids: ids of products to get

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
            since: from what time
            before: to what time
            user_id: target user id

        Returns: list of transactions

        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, tid: TransactionId) -> Transaction:
        """
        Get transaction by id.

        Args:
            tid: transaction id

        Returns: transaction

        Raises:
            TransactionNotFound

        """
        raise NotImplementedError
