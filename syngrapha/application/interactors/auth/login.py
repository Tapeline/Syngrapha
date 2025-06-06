from typing import final

from syngrapha.application.auth.auth import (
    AuthToken,
    UserCredentialStore,
)
from syngrapha.application.auth.exceptions import UserCredsNotFound
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.uow import UoW
from syngrapha.utils.decorator import impl


@interactor
@final
class LoginInteractor:
    """Login a user and return auth token."""

    user_cred_store: UserCredentialStore
    uow: UoW

    @impl
    async def __call__(
            self,
            username: str,
            password: str
    ) -> AuthToken:
        async with self.uow:
            user_id = await self.user_cred_store.login_user(
                username, password
            )
            if not user_id:
                raise UserCredsNotFound
            return await self.user_cred_store.generate_token(user_id)
