from typing import final

from syngrapha.application.auth.auth import UserIdProvider
from syngrapha.application.external.nalog import NalogClient
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.user import UserGateway
from syngrapha.utils.decorator import impl


@interactor
@final
class RequestNalogAuthCodeInteractor:
    """Start process of authenticating at nalog.ru."""

    nalog_client: NalogClient
    user_gw: UserGateway
    user_idp: UserIdProvider

    @impl
    async def __call__(self) -> None:
        user_id = await self.user_idp.get_user()
        user = await self.user_gw.get_by_id(user_id)
        await self.nalog_client.request_auth(user.phone_number)
