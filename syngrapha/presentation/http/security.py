from types import MappingProxyType
from typing import Any, Final

from litestar import Request
from litestar.openapi.spec import SecurityScheme

from syngrapha.application.auth.auth import (
    TokenCredStoreIdProvider,
    UserCredentialStore, UserIdProvider,
)

security_components: Final = {
    "jwt_auth": SecurityScheme(
        type="apiKey",
        name="Authorization",
        security_scheme_in="header",
    ),
    "cookie_auth": SecurityScheme(
        type="apiKey",
        security_scheme_in="cookie",
        name="SESSION_ID"
    )
}

security_defs: Final = (
    {"jwt_auth": []},
    {"cookie_auth": []}
)


def authenticate_user(
        cred_store: UserCredentialStore,
        request: Request[Any, Any, Any]
) -> UserIdProvider:
    """Create user identity provider using data supplied in request."""
    auth_header = request.headers.get("authorization")
    if auth_header:
        auth_header = str(auth_header).removeprefix("Bearer").strip()
    session_id = request.cookies.get("SESSION_ID")
    return TokenCredStoreIdProvider(
        cred_store=cred_store,
        token=auth_header or session_id or ""
    )
