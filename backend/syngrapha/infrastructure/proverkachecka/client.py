import datetime
import uuid
from dataclasses import dataclass
from decimal import Decimal
from typing import final

from aiohttp import ClientSession

from syngrapha.application.external.checks import SimpleCheckLoader
from syngrapha.application.external.nalog import (
    NalogReceipt,
    NalogReceiptItem, NalogReturnedError,
)
from syngrapha.config import ProverkaChekaConfig
from syngrapha.domain.money import Money
from syngrapha.utils.decorator import impl


@dataclass
@final
class ProxiedProverkaChekaClient(SimpleCheckLoader):
    config: ProverkaChekaConfig

    @impl
    async def get_receipt(self, code: str) -> NalogReceipt:
        async with (
            ClientSession() as session,
            session.get(
                f"{self.config.base_url}/get-check?{code}",
            ) as response
        ):
            if response.status // 100 != 2:
                raise NalogReturnedError
            data = await response.json()
            try:
                return _load_receipt(data)
            except KeyError as exc:
                raise NalogReturnedError from exc


def _load_receipt(data: list[str | list[str]]) -> NalogReceipt:
    created_at, store_name, store_addr, total, items = data
    items = [
        NalogReceiptItem(
            name=name,
            quantity=float(qty),
            price=Money.from_decimal(
                Decimal(price),
                multiplier=100
            )
        )
        for name, price, qty, _ in items
    ]
    return NalogReceipt(
        id=uuid.uuid4(),
        created_at=datetime.datetime.fromisoformat(created_at),
        merchant=store_name,
        items=items
    )
