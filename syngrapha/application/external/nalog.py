import uuid
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from syngrapha.domain.money import Money
from syngrapha.domain.user import NalogToken, PhoneNumber


class NalogClientException(Exception):
    """Base class for all nalog client exceptions."""


class NalogTokenRequiresReAuth(NalogClientException):
    """Raised when nalog.ru token expired."""


class NalogReturnedError(NalogClientException):
    """Raised when nalog.ru returned smth unexpected."""


@dataclass
class NalogReceiptItem:
    """Represents a single item in receipt."""

    name: str
    price: Money
    quantity: int


@dataclass
class NalogReceipt:
    """Represents a single receipt."""

    id: uuid.UUID
    created_at: datetime
    items: list[NalogReceiptItem]
    merchant: str


class NalogClient(Protocol):
    """Interface for interacting with nalog.ru's IRKKT."""

    @abstractmethod
    async def check_token_valid(self, access_token: NalogToken) -> bool:
        """Check if access token is valid."""

    @abstractmethod
    async def request_auth(self, phone: PhoneNumber) -> None:
        """
        Request authentication with SMS code.

        Args:
            phone: target phone

        """

    @abstractmethod
    async def submit_auth_code(
            self,
            phone: PhoneNumber,
            code: str
    ) -> NalogToken | None:
        """
        Try to authenticate with SMS code.

        Args:
            phone: target phone
            code: SMS secret code

        Returns:
            NalogToken if authentication succeeded
            None otherwise

        """

    @abstractmethod
    async def get_receipt(
            self,
            access_token: NalogToken,
            code: str
    ) -> NalogReceipt:
        """Get receipt by its code."""
