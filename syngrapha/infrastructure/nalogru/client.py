from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Final, final

from aiohttp import ClientSession

from syngrapha.application.external.nalog import (
    NalogClient,
    NalogReceipt,
    NalogReceiptItem, NalogReturnedError, NalogTokenRequiresReAuth,
)
from syngrapha.config import NalogConfig
from syngrapha.domain.money import Money
from syngrapha.domain.user import NalogToken, PhoneNumber

_BASE_URL: Final = "https://irkkt-mobile.nalog.ru:8888/v2"


@final
@dataclass(slots=True)
class NalogClientImpl(NalogClient):
    """Impl."""

    config: NalogConfig

    async def check_token_valid(self, access_token: NalogToken) -> bool:
        async with ClientSession() as session:
            # Send a dummy request for ticket to check the token
            async with session.post(
                f"{_BASE_URL}/ticket",
                json={"qr": ""},
                headers={"sessionId": access_token or ""}
            ) as response:
                return response.status != 401

    async def request_auth(self, phone: PhoneNumber) -> None:
        async with ClientSession() as session:
            async with session.post(
                f"{_BASE_URL}/auth/phone/request",
                json={
                    "phone": phone,
                    "client_secret": self.config.secret,
                    "os": "Android",
                },
            ) as response:
                await response.text()
                if response.status // 100 != 2:
                    raise NalogReturnedError

    async def submit_auth_code(
            self,
            phone: PhoneNumber,
            code: str
    ) -> NalogToken | None:
        async with ClientSession() as session:
            async with session.post(
                f"{_BASE_URL}/auth/phone/verify",
                json={
                    "phone": phone,
                    "client_secret": self.config.secret,
                    "os": "Android",
                    "code": code
                },
            ) as response:
                data = await response.json()
                if response.status // 100 != 2:
                    return None
                return data.get("sessionId")

    async def _get_receipt_id(
            self,
            access_token: NalogToken,
            code: str,
            session: ClientSession
    ) -> str:
        async with session.post(
            f"{_BASE_URL}/ticket",
            json={"qr": code},
            headers={"sessionId": access_token}
        ) as response:
            data = await response.json()
            if response.status == 401:
                raise NalogTokenRequiresReAuth
            elif response.status // 100 != 2:
                raise NalogReturnedError
            return data["id"]

    async def get_receipt(
            self,
            access_token: NalogToken,
            code: str
    ) -> NalogReceipt:
        async with ClientSession() as session:
            ticket_id = await self._get_receipt_id(
                access_token, code, session
            )
            async with session.get(
                f"{_BASE_URL}/tickets/{ticket_id}",
                headers={
                    "sessionId": access_token,
                    "Content-Type": "application/json"
                }
            ) as response:
                data = await response.json()
                if response.status == 401:
                    raise NalogTokenRequiresReAuth
                elif response.status // 100 != 2:
                    raise NalogReturnedError
                try:
                    return _load_receipt(data)
                except KeyError:
                    raise NalogReturnedError


def _load_receipt(data: dict[str, Any]) -> NalogReceipt:
    t_id = data["id"]
    created_at = data["operation"]["date"]
    receipt = data["ticket"]["document"]["receipt"]
    merchant = receipt["retailPlace"]
    items = [
        NalogReceiptItem(
            name=item["name"],
            quantity=item["quantity"],
            price=Money.from_decimal(
                Decimal(item["price"]) / Decimal(100),
                multiplier=100
            )
        )
        for item in receipt["items"]
    ]
    return NalogReceipt(
        id=t_id,
        created_at=created_at,
        merchant=merchant,
        items=items
    )
