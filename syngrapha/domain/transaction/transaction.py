import operator
import uuid
from collections.abc import Collection
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from functools import reduce
from typing import Any, final

from syngrapha.domain.money import Money
from syngrapha.domain.product.product import Product
from syngrapha.domain.user import UserId

type TransactionId = uuid.UUID
type MerchantName = str

_TRANSACTION_EQ_DELTA_S = 5


@dataclass(slots=True)
@final
class Transaction:
    """Defines transaction domain model."""

    id: TransactionId
    products: list[Product]
    time_of_deal: datetime
    merchant: MerchantName
    owner: UserId

    @property
    def cost(self) -> Money:
        """Calculated cost (sum of products' costs)."""
        return Money.from_decimal(reduce(
            operator.add,
            (product.cost for product in self.products),
            Decimal(0)
        ))

    def __eq__(self, other: Any) -> bool:
        """Is equal to other transaction."""
        if not isinstance(other, Transaction):
            return NotImplemented
        self_time = int(self.time_of_deal.timestamp())
        other_time = int(other.time_of_deal.timestamp())
        return (
            abs(self_time - other_time) < _TRANSACTION_EQ_DELTA_S
            and self.cost == other.cost
        )

    def __hash__(self) -> int:
        """Hash the transaction."""
        return hash((
            #int(self.time_of_deal.timestamp()),
            int(self.cost.as_float * self.cost.multiplier),
        ))


def deduplicate_transactions(
        *transactions: Collection[Transaction]
) -> Collection[Transaction]:
    """Deduplicates transactions using set."""
    t_set: set[Transaction] = set()
    for transaction_collection in transactions:
        t_set.update(transaction_collection)
    return t_set
