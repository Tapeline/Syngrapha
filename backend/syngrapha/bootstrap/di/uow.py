from collections.abc import AsyncIterable

from dishka import Provider, Scope, WithParents, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from syngrapha.config import Config
from syngrapha.infrastructure.persistence.database import new_session_maker
from syngrapha.infrastructure.persistence.uow import SAUoW


class UoWDIProvider(Provider):
    """Provides sessions and UoWs."""

    @provide(scope=Scope.APP)
    def get_session_maker(
            self, config: Config
    ) -> async_sessionmaker[AsyncSession]:
        """Provide app session maker."""
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_uow(
            self,
            session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[WithParents[SAUoW]]:
        """Provide UoW."""
        async with session_maker() as session:
            yield SAUoW(session)
