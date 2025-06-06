from abc import abstractmethod
from typing import Any, Protocol


class UoW(Protocol):
    """A unit of work."""

    @abstractmethod
    async def __aenter__(self) -> None:
        """Init UoW."""

    @abstractmethod
    async def __aexit__(
            self,
            exc_type: type[Exception],
            exc_val: Exception,
            exc_tb: Any
    ) -> None:
        """Rollback or commit."""
