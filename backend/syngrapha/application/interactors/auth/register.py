from typing import final

from syngrapha.application.auth.auth import UserCredentialStore
from syngrapha.application.identifier import UUIDGenerator
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.uow import UoW
from syngrapha.domain.user import User
from syngrapha.utils.decorator import impl


@interactor
@final
class RegisterInteractor:
    """Register a user."""

    user_cred_store: UserCredentialStore
    id_gen: UUIDGenerator
    uow: UoW

    @impl
    async def __call__(
            self,
            username: str,
            phone_number: str,
            password: str
    ) -> User:
        async with self.uow:
            user = User(
                id=self.id_gen(),
                username=username,
                phone_number=phone_number,
                nalog_access_token=None,
            )
            await self.user_cred_store.register_user(user, password)
            return user
