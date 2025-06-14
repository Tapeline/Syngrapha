from abc import abstractmethod
from collections.abc import Collection
from datetime import datetime
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
