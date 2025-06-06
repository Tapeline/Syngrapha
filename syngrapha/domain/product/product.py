import enum
import uuid
from dataclasses import dataclass
from typing import final

from syngrapha.domain.money import Money
from syngrapha.domain.product.category import Category

type ProductId = uuid.UUID
type ProductName = str
type ItemQuantity = int


@final
class AutoCategorizingState(enum.Enum):
    """State of autocategorizer on that product."""

    IN_PROCESS = enum.auto()
    MARKED = enum.auto()


@dataclass(slots=True)
@final
class Product:
    """Defines a product domain model."""

    id: ProductId
    product: ProductName
    quantity: ItemQuantity
    category: Category | None
    price: Money
    auto_cat_state: AutoCategorizingState

    @property
    def cost(self) -> Money:
        """Calculated cost from price and quantity."""
        return Money.from_decimal(self.price.as_decimal * self.quantity)
