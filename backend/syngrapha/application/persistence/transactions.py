from abc import abstractmethod
from collections.abc import Collection
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from syngrapha.domain.transaction.transaction import Transaction, TransactionId
from syngrapha.domain.product.product import ProductId
from syngrapha.domain.user import UserId


@dataclass
class TransactionNotFound(Exception):
    id: TransactionId


@dataclass
class TransactionAccessDenied(Exception):
    id: TransactionId


@dataclass
class ProductNotFound(Exception):
    transaction_id: TransactionId
    product_id: ProductId


class TransactionGateway(Protocol):
    """Access to transaction store."""

    @abstractmethod
    async def save_transaction(self, transaction: Transaction) -> None:
        """
        Save single transaction (create or update).

        Args:
            transaction: transaction to save.

        """
        raise NotImplementedError

    @abstractmethod
    async def get_of_user(
            self,
            user_id: UserId,
            since: datetime | None = None,
            before: datetime | None = None
    ) -> Collection[Transaction]:
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
