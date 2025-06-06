from dataclasses import dataclass

from adaptix import P
from adaptix.conversion import get_converter, link, coercer
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from syngrapha.application.auth.exceptions import UserNotFound
from syngrapha.application.persistence.user import UserGateway
from syngrapha.domain.user import User, UserId
from syngrapha.infrastructure.persistence.models import UserModel
from syngrapha.infrastructure.persistence.uow import SAUoW
from syngrapha.utils.coerce import id_link
from syngrapha.utils.decorator import impl
from syngrapha.utils.func import identity


_convert_user = get_converter(
    src=UserModel,
    dst=User,
    recipe=[
        id_link(P[UserModel].uuid, P[User].id),
        id_link(P[UserModel].phone_number, P[User].phone_number),
        id_link(P[UserModel].nalog_access_token, P[User].nalog_access_token),
    ],
)


@dataclass
class UserGatewayImpl(UserGateway):
    """Impl."""

    uow: SAUoW

    @impl
    async def get_by_id(self, uid: UserId) -> User:
        query = select(UserModel).where(UserModel.uuid == uid)
        result = await self.uow.session.execute(query)
        try:
            return _convert_user(result.scalars().one())
        except NoResultFound as exc:
            raise UserNotFound(uid) from exc
