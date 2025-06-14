from typing import Any, final

from sqlalchemy.ext.asyncio import AsyncSession

from syngrapha.application.persistence.uow import UoW
from syngrapha.utils.decorator import impl


@final
class SAUoW(UoW):
    """Impl."""

    def __init__(self, session: AsyncSession):
        """Init the UoW."""
        self.session = session

    @impl
    async def __aenter__(self) -> None:
        pass  # noqa: WPS420

    @impl
    async def __aexit__(
            self,
            exc_type: type[Exception],
            exc_val: Exception,
            exc_tb: Any
    ) -> None:
        if exc_val:
            await self.session.rollback()
        else:
            await self.session.commit()
