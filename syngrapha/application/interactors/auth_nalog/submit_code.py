from typing import final

from syngrapha.application.auth.auth import UserIdProvider
from syngrapha.application.external.nalog import NalogClient
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.uow import UoW
from syngrapha.application.persistence.user import UserGateway
from syngrapha.domain.user import NalogToken
from syngrapha.utils.decorator import impl


class InvalidNalogSMSCode(Exception):
    """Raised when entered SMS code is invalid."""


@interactor
@final
class SubmitNalogAuthCodeInteractor:
    """Finish login with nalog.ru."""

    nalog_client: NalogClient
    user_gw: UserGateway
    user_idp: UserIdProvider
    uow: UoW

    @impl
    async def __call__(self, code: str) -> NalogToken:
        user_id = await self.user_idp.get_user()
        user = await self.user_gw.get_by_id(user_id)
        token = await self.nalog_client.submit_auth_code(
            user.phone_number, code
        )
        if not token:
            raise InvalidNalogSMSCode
        user.nalog_access_token = token
        async with self.uow:
            await self.user_gw.save_user(user)
        return token
