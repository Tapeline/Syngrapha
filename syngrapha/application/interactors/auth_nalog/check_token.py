from typing import final

from syngrapha.application.auth.auth import UserIdProvider
from syngrapha.application.external.nalog import NalogClient
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.user import UserGateway


@interactor
@final
class CheckNalogAuthTokenInteractor:
    nalog_client: NalogClient
    user_gw: UserGateway
    user_idp: UserIdProvider

    async def __call__(self) -> bool:
        user_id = await self.user_idp.get_user()
        user = await self.user_gw.get_by_id(user_id)
        return await self.nalog_client.check_token_valid(
            user.nalog_access_token
        )
