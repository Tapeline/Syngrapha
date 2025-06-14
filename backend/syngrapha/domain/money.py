from decimal import Decimal
from typing import Any, Final, final

from syngrapha.domain.vo import value_object

MULTIPLIER: Final = 100


@value_object
@final
class Money:
    """Represents some amount of money."""

    value: int
    multiplier: int

    @property
    def as_x100_int(self) -> int:
        """Return representation as int(self * 100) (x100 format)."""
        canonical_value = self.as_decimal
        return int((canonical_value * 100).to_integral_value())

    @property
    def as_float(self) -> float:
        """Return float representation."""
        return self.value / self.multiplier

    @property
    def as_decimal(self) -> Decimal:
        """Return Decimal representation."""
        return Decimal(self.value) / Decimal(self.multiplier)

    @classmethod
    def from_decimal(
            cls,
            decimal: Decimal,
            multiplier: int = MULTIPLIER
    ) -> "Money":
        """Parse money from decimal."""
        value = int((decimal * multiplier).to_integral_exact())
        return Money(value=value, multiplier=multiplier)

    @classmethod
    def from_float(
            cls,
            value: float,
            multiplier: int = MULTIPLIER
    ) -> "Money":
        """Parse money from float."""
        return Money(value=int(value * multiplier), multiplier=multiplier)

    def __eq__(self, other: Any) -> bool:
        """Eq impl."""
        if not isinstance(other, Money):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other: Any) -> bool:
        """Neq impl."""
        if not isinstance(other, Money):
            return NotImplemented
        return not (self == other)
