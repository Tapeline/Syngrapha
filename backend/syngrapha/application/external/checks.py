from abc import abstractmethod
from typing import Protocol

from syngrapha.application.external.nalog import NalogReceipt


class SimpleCheckLoader(Protocol):
    @abstractmethod
    async def get_receipt(
            self,
            code: str
    ) -> NalogReceipt:
        """Get receipt by its code."""
