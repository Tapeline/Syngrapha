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
