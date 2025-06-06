from dataclasses import dataclass

from adaptix import P, Retort
from adaptix.conversion import get_converter, link, coercer
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from syngrapha.application.auth.exceptions import UserNotFound
from syngrapha.application.persistence.user import UserGateway
from syngrapha.domain.user import User, UserId
from syngrapha.infrastructure.persistence.models import UserModel
from syngrapha.infrastructure.persistence.uow import SAUoW
from syngrapha.utils.coerce import id_link
from syngrapha.utils.decorator import impl


_convert_user = get_converter(
    src=UserModel,
    dst=User,
    recipe=[
        id_link(P[UserModel].uuid, P[User].id),
        id_link(P[UserModel].phone_number, P[User].phone_number),
        id_link(P[UserModel].nalog_access_token, P[User].nalog_access_token),
    ],
)
_user_retort = Retort()


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

    @impl
    async def save_user(self, user: User) -> None:
        query = (
            update(UserModel)
            .where(UserModel.uuid == user.id)
            .values(
                nalog_access_token=user.nalog_access_token,
                phone_number=user.phone_number
            )
        )
        try:
            await self.uow.session.execute(query)
        except NoResultFound as exc:
            raise UserNotFound(user.id) from exc
