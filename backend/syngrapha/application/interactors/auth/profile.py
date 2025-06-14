from typing import final

from syngrapha.application.auth.auth import UserIdProvider
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.uow import UoW
from syngrapha.application.persistence.user import UserGateway
from syngrapha.domain.user import User
from syngrapha.utils.decorator import impl


@interactor
@final
class GetProfileInteractor:
    """Get user's profile."""

    uow: UoW
    user_gw: UserGateway
    user_idp: UserIdProvider

    @impl
    async def __call__(self) -> User:
        async with self.uow:
            return await self.user_gw.get_by_id(
                await self.user_idp.get_user()
            )
