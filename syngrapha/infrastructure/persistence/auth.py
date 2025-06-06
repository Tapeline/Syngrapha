import uuid
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, cast, final

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from syngrapha.application.auth.auth import (
    AuthToken,
    UserCredentialStore,
)
from syngrapha.application.auth.exceptions import UserAlreadyExists
from syngrapha.config import SecurityConfig
from syngrapha.domain.user import User, UserId
from syngrapha.infrastructure.persistence.models import (
    UserAuthTokenModel,
    UserModel,
)
from syngrapha.infrastructure.persistence.uow import SAUoW
from syngrapha.utils.decorator import impl


class PasswordHasher(Protocol):
    """Hash algorithm."""

    @abstractmethod
    def __call__(self, password: str) -> str:
        """
        Hash the password.

        Args:
            password: target password

        Returns: hashed password

        """


class PasswordHashComparator(Protocol):
    """Hashed pass comparator."""

    @abstractmethod
    def __call__(self, hashed: str, password: str) -> bool:
        """
        Compare hashed and raw password.

        Args:
            hashed: hashed password
            password: raw password

        Returns:
            are same?

        """


class AuthTokenGenerator(Protocol):
    """Auth token generator."""

    @abstractmethod
    def __call__(self) -> str:
        """
        Generate auth token.

        Returns: secure and random auth token.

        """


@dataclass(slots=True, frozen=True)
@final
class UserCredentialStoreImpl(UserCredentialStore):
    """Impl."""

    uow: SAUoW
    password_hasher: PasswordHasher
    password_comparator: PasswordHashComparator
    token_gen: AuthTokenGenerator
    sec_conf: SecurityConfig

    @impl
    async def register_user(self, user: User, password: str) -> None:
        query = insert(UserModel).values(
            uuid=str(user.id),
            username=user.username,
            hashed_pass=self.password_hasher(password),
            nalog_access_token=user.nalog_access_token,
            phone_number=user.phone_number,
        )
        try:
            await self.uow.session.execute(query)
        except IntegrityError as exc:
            raise UserAlreadyExists(user.username) from exc

    @impl
    async def login_user(self, username: str, password: str) -> UserId | None:
        query = select(UserModel).where(
            UserModel.username == username
        )
        result = await self.uow.session.execute(query)
        user = result.scalars().first()
        if not user:
            return None
        return (
            uuid.UUID(user.uuid)
            if self.password_comparator(user.hashed_pass, password)
            else None
        )

    @impl
    async def authorize(self, token: AuthToken) -> UserId | None:
        expiry = datetime.now() - self.sec_conf.token_lifetime
        query = select(UserAuthTokenModel).where(
            UserAuthTokenModel.token == token,
            UserAuthTokenModel.issued_at > expiry
        )
        result = await self.uow.session.execute(query)
        token_model = result.scalars().first()
        if not token_model:
            return None
        return cast(uuid.UUID, token_model.user_id)

    @impl
    async def generate_token(self, user_id: UserId) -> AuthToken:
        token = self.token_gen()
        query = insert(UserAuthTokenModel).values(
            user_id=user_id,
            token=token
        )
        await self.uow.session.execute(query)
        return token

    @impl
    async def revoke_tokens(self, user_id: UserId) -> None:
        query = delete(UserAuthTokenModel).where(
            UserAuthTokenModel.user_id == user_id
        )
        await self.uow.session.execute(query)
