import secrets
from typing import Final

import argon2
from argon2.exceptions import VerifyMismatchError

from syngrapha.infrastructure.persistence.auth import (
    AuthTokenGenerator,
    PasswordHashComparator,
    PasswordHasher,
)
from syngrapha.utils.decorator import impl

_AUTH_TOKEN_BYTE_LEN: Final = 32


class ArgonHasher(PasswordHasher):
    """Impl."""

    @impl
    def __call__(self, password: str) -> str:
        return argon2.hash_password(password.encode()).decode()


class ArgonComparator(PasswordHashComparator):
    """Impl."""

    @impl
    def __call__(self, hashed: str, password: str) -> bool:
        try:
            return argon2.verify_password(hashed.encode(), password.encode())
        except VerifyMismatchError:
            return False


class SecretsTokenGenerator(AuthTokenGenerator):
    """Impl."""

    @impl
    def __call__(self) -> str:
        return secrets.token_hex(_AUTH_TOKEN_BYTE_LEN)
