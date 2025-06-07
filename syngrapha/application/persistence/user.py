from abc import abstractmethod
from typing import Protocol

from syngrapha.domain.user import User, UserId


class UserGateway(Protocol):
    """Access to users."""

    @abstractmethod
    async def get_by_id(self, uid: UserId) -> User:
        """
        Get user by its id.

        Args:
            uid: target id

        Returns:
            found user

        Raises:
            UserNotFound: if user is not found

        """
        raise NotImplementedError

    @abstractmethod
    async def save_user(self, user: User) -> None:
        """
        Save user model.

        Args:
            user: target user

        """
        raise NotImplementedError

    @abstractmethod
    async def lock(self, user_id: UserId) -> None:
        """
        Lock user by its id.

        Args:
            user_id: target user id

        """
        raise NotImplementedError
