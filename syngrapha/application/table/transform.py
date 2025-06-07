from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
from types import MappingProxyType
from typing import Final, Mapping, Any

from syngrapha.domain.money import Money

type Transformer[T] = Callable[[str], T]


def money_tf(data: str) -> Money:
    """Transform money into x100 format"""
    dec = Decimal(data) / 100
    return Money.from_decimal(dec, multiplier=100)


def iso_date_tf(data: str) -> datetime:
    """Transform ISO datetime."""
    return datetime.fromisoformat(data)


def int_tf(data: str) -> int:
    """Transform int."""
    return int(data)


TRANSFORMERS: Final[Mapping[str, Transformer[Any]]] = MappingProxyType({
    "money": money_tf,
    "iso_date": iso_date_tf,
    "int": int_tf,
})
