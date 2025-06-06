from dishka import Provider, Scope, provide, provide_all

from syngrapha.application.auth.auth import UserCredentialStore
from syngrapha.application.interactors.auth.login import LoginInteractor
from syngrapha.application.interactors.auth.logout import \
    RevokeTokensInteractor
from syngrapha.application.interactors.auth.profile import GetProfileInteractor
from syngrapha.application.interactors.auth.register import RegisterInteractor
from syngrapha.application.persistence.user import UserGateway
from syngrapha.infrastructure.persistence.auth import UserCredentialStoreImpl
from syngrapha.infrastructure.persistence.user_gw import UserGatewayImpl


class UserDIProvider(Provider):
    """Provides everything related to users."""

    interactors = provide_all(
        LoginInteractor,
        RegisterInteractor,
        GetProfileInteractor,
        RevokeTokensInteractor,
        scope=Scope.REQUEST,
    )
    user_gateway = provide(
        UserGatewayImpl, provides=UserGateway, scope=Scope.REQUEST
    )
    user_cred = provide(
        UserCredentialStoreImpl,
        provides=UserCredentialStore,
        scope=Scope.REQUEST
    )
