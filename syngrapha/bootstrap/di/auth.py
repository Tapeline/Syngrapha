from dishka import Provider, Scope, provide
from litestar import Request

from syngrapha.application.auth.auth import (
    UserCredentialStore,
    UserIdProvider,
)
from syngrapha.presentation.http.security import authenticate_user


class AuthTokenDIProvider(Provider):
    """Provider of id provider."""

    @provide(scope=Scope.REQUEST)
    def provide_identity(
            self,
            request: Request,  # type: ignore
            cred_store: UserCredentialStore,
    ) -> UserIdProvider:
        """Create identity provider from request headers or cookies."""
        return authenticate_user(cred_store, request)
