from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Final, final

from aiohttp import ClientSession
from litestar.status_codes import HTTP_401_UNAUTHORIZED

from syngrapha.application.external.nalog import (
    NalogClient,
    NalogReceipt,
    NalogReceiptItem,
    NalogReturnedError,
    NalogTokenRequiresReAuth,
)
from syngrapha.config import NalogConfig
from syngrapha.domain.money import Money
from syngrapha.domain.user import NalogToken, PhoneNumber
from syngrapha.utils.decorator import impl

_BASE_URL: Final = "https://irkkt-mobile.nalog.ru:8888/v2"
_SESSON_HEADER: Final = "sessionId"


@final
@dataclass(slots=True)
class NalogClientImpl(NalogClient):
    """Impl."""

    config: NalogConfig

    @impl
    async def check_token_valid(
            self, access_token: NalogToken | None
    ) -> bool:
        if not access_token:
            return False
        async with (
            ClientSession() as session,
            session.post(
                f"{_BASE_URL}/ticket",
                json={"qr": ""},
                headers={_SESSON_HEADER: access_token or ""}
            ) as response
        ):
            # Send a dummy request for ticket to check the token
            return response.status != HTTP_401_UNAUTHORIZED

    @impl
    async def request_auth(self, phone: PhoneNumber) -> None:
        async with (
            ClientSession() as session,
            session.post(
                f"{_BASE_URL}/auth/phone/request",
                json={
                    "phone": phone,
                    "client_secret": self.config.secret,
                    "os": "Android",
                },
            ) as response
        ):
            text = await response.text()
            if response.status // 100 != 2:
                raise NalogReturnedError

    @impl
    async def submit_auth_code(
            self,
            phone: PhoneNumber,
            code: str
    ) -> NalogToken | None:
        async with (
            ClientSession() as session,
            session.post(
                f"{_BASE_URL}/auth/phone/verify",
                json={
                    "phone": phone,
                    "client_secret": self.config.secret,
                    "os": "Android",
                    "code": code
                },
            ) as response
        ):
            if response.status // 100 != 2:
                return None
            data = await response.json()
            session_id = data.get(_SESSON_HEADER)
            return str(session_id) if session_id else None

    @impl
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
                if response.status == HTTP_401_UNAUTHORIZED:
                    raise NalogTokenRequiresReAuth
                if response.status // 100 != 2:
                    raise NalogReturnedError
                data = await response.json()
                try:
                    return _load_receipt(data)
                except KeyError as exc:
                    raise NalogReturnedError from exc

    @impl
    async def _get_receipt_id(
            self,
            access_token: NalogToken,
            code: str,
            session: ClientSession
    ) -> str:
        async with session.post(
            f"{_BASE_URL}/ticket",
            json={"qr": code},
            headers={_SESSON_HEADER: access_token}
        ) as response:
            if response.status == HTTP_401_UNAUTHORIZED:
                raise NalogTokenRequiresReAuth
            if response.status // 100 != 2:
                raise NalogReturnedError
            data = await response.json()
            return str(data["id"])


def _load_receipt(data: dict[str, Any]) -> NalogReceipt:
    t_id = data["id"]
    created_at = data["operation"]["date"]
    receipt = data["ticket"]["document"]["receipt"]
    merchant = receipt["retailPlace"]
    items = [
        NalogReceiptItem(
            name=receipt_item["name"],
            quantity=receipt_item["quantity"],
            price=Money.from_decimal(
                Decimal(receipt_item["price"]) / Decimal(100),
                multiplier=100
            )
        )
        for receipt_item in receipt["items"]
    ]
    return NalogReceipt(
        id=t_id,
        created_at=created_at,
        merchant=merchant,
        items=items
    )
