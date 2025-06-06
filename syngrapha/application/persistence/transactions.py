from abc import abstractmethod
from typing import Protocol

from syngrapha.domain.transaction.transaction import Transaction


class TransactionGateway(Protocol):
    """Access to transaction store."""

    @abstractmethod
    async def save_transaction(self, transaction: Transaction) -> None:
        """Save single transaction (create or update)."""
