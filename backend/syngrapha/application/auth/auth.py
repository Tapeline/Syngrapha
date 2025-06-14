from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, final

from syngrapha.application.auth.exceptions import UserNotAuthenticated
from syngrapha.domain.user import User, UserId
from syngrapha.utils.decorator import impl

type AuthToken = str


class UserIdProvider(Protocol):
    """Provides user identity."""

    @abstractmethod
    async def get_user(self) -> UserId:
        """
        Try to authorize user and return it.

        Returns: authorized user id

        Raises:
            UserNotAuthenticated: if user is not authenticated

        """
        raise NotImplementedError


class UserCredentialStore(Protocol):
    """Manage user authentication and credentials."""

    @abstractmethod
    async def register_user(self, user: User, password: str) -> None:
        """
        Register a user and assign password.

        Args:
            user: target user
            password: UNHASHED password

        Raises:
            UserAlreadyExists: if attempted username already exists

        """
        raise NotImplementedError

    @abstractmethod
    async def login_user(self, username: str, password: str) -> UserId | None:
        """
        Check that inputted password is valid.

        Args:
            username: target username
            password: UNHASHED password

        Returns:
            id of logged user or None if credentials are incorrect

        """
        raise NotImplementedError

    @abstractmethod
    async def authorize(self, token: AuthToken) -> UserId | None:
        """
        Authorize some user by token.

        Args:
            user_id: target user
            token: its access token

        Returns:
            whether the token in valid

        """
        raise NotImplementedError

    @abstractmethod
    async def generate_token(self, user_id: UserId) -> AuthToken:
        """
        Generate new auth token for user.

        Args:
            user_id: target user id

        Returns:
            new token

        """
        raise NotImplementedError

    @abstractmethod
    async def revoke_tokens(self, user_id: UserId) -> None:
        """
        Revoke all tokens from user.

        Args:
            user_id: target user

        """
        raise NotImplementedError


@dataclass(slots=True, frozen=True)
@final
class TokenCredStoreIdProvider(UserIdProvider):
    """Id provider impl. Needs to have token injected."""

    cred_store: UserCredentialStore
    token: AuthToken

    @impl
    async def get_user(self) -> UserId:
        user_id = await self.cred_store.authorize(self.token)
        if not user_id:
            raise UserNotAuthenticated
        return user_id
