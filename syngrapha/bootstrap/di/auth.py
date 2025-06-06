
from dishka import Provider, Scope, provide
from litestar import Request

from syngrapha.application.auth.auth import (
    TokenCredStoreIdProvider,
    UserCredentialStore,
    UserIdProvider,
)


class HeaderTokenDIProvider(Provider):
    """Provider of id provider."""

    @provide(scope=Scope.REQUEST)
    def provide_identity(
            self,
            request: Request,  # type: ignore
            cred_store: UserCredentialStore,
    ) -> UserIdProvider:
        """Create identity provider from request headers."""
        auth_header = request.headers.get("authorization")
        if auth_header:
            auth_header = str(auth_header).removeprefix("Bearer").strip()
        return TokenCredStoreIdProvider(
            cred_store=cred_store,
            token=auth_header or ""
        )
