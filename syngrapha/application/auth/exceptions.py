from syngrapha.domain.user import UserId


class UserException(Exception):
    """Base user exception."""


class UserNotAuthenticated(UserException):
    """Raised when user is not authenticated."""


class UserCredsNotFound(UserException):
    """Raised when user with such creds is not found."""


class UserNotFound(UserException):
    """Raised when user with such id is not found."""

    def __init__(self, uid: UserId) -> None:
        """Init and set uid."""
        self.id = uid


class UserAlreadyExists(UserException):
    """Raised when user with such username already exists."""

    def __init__(self, username: str) -> None:
        """Init and set username."""
        self.username = username
