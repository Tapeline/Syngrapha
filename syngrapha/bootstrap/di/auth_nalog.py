from dishka import Provider, Scope, provide_all

from syngrapha.application.interactors.auth_nalog.check_token import \
    CheckNalogAuthTokenInteractor
from syngrapha.application.interactors.auth_nalog.request_code import \
    RequestNalogAuthCodeInteractor
from syngrapha.application.interactors.auth_nalog.submit_code import \
    SubmitNalogAuthCodeInteractor


class AuthNalogDIProvider(Provider):
    """Provider of everything for nalog.ru auth."""

    interactors = provide_all(
        RequestNalogAuthCodeInteractor,
        SubmitNalogAuthCodeInteractor,
        CheckNalogAuthTokenInteractor,
        scope=Scope.REQUEST
    )
