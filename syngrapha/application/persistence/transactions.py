from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol

from syngrapha.domain.transaction.transaction import Transaction
from syngrapha.domain.user import UserId


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
    async def get_of_user(self, user_id: UserId) -> Collection[Transaction]:
        """
        Get all transactions owned by the given user.

        Args:
            user_id: target user id

        Returns: list of transactions

        """
        raise NotImplementedError
