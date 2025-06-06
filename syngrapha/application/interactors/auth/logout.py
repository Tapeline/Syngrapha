from typing import final

from syngrapha.application.auth.auth import UserCredentialStore, UserIdProvider
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.uow import UoW
from syngrapha.utils.decorator import impl


@interactor
@final
class RevokeTokensInteractor:
    """Revoke all user's auth tokens."""

    uow: UoW
    user_idp: UserIdProvider
    cred_store: UserCredentialStore

    @impl
    async def __call__(self) -> None:
        user_id = await self.user_idp.get_user()
        async with self.uow:
            await self.cred_store.revoke_tokens(user_id)
