from dishka import Provider, Scope, provide

from syngrapha.application.identifier import UUIDGenerator
from syngrapha.infrastructure.identifier import UUIDGeneratorImpl
from syngrapha.infrastructure.persistence.auth import (
    AuthTokenGenerator,
    PasswordHashComparator,
    PasswordHasher,
)
from syngrapha.infrastructure.security import (
    ArgonComparator,
    ArgonHasher,
    SecretsTokenGenerator,
)


class AlgorithmsDIProvider(Provider):
    """Provides different algorithms."""

    scope = Scope.APP

    hasher = provide(ArgonHasher, provides=PasswordHasher)
    hash_cmp = provide(ArgonComparator, provides=PasswordHashComparator)
    id_gen = provide(UUIDGeneratorImpl, provides=UUIDGenerator)
    token_gen = provide(SecretsTokenGenerator, provides=AuthTokenGenerator)
