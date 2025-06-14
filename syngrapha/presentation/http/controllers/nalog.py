import uuid

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post
from pydantic import BaseModel

from syngrapha.application.interactors.auth.login import LoginInteractor
from syngrapha.application.interactors.auth.logout import (
    RevokeTokensInteractor,
)
from syngrapha.application.interactors.auth.profile import GetProfileInteractor
from syngrapha.application.interactors.auth.register import RegisterInteractor
from syngrapha.application.interactors.auth_nalog.check_token import \
    CheckNalogAuthTokenInteractor
from syngrapha.application.interactors.auth_nalog.request_code import \
    RequestNalogAuthCodeInteractor
from syngrapha.application.interactors.auth_nalog.submit_code import \
    SubmitNalogAuthCodeInteractor
from syngrapha.presentation.http.framework.openapi import (
    error_spec,
    success_spec,
)
from syngrapha.presentation.http.security import security_defs


class SubmitCodeSchema(BaseModel):
    code: str


class TokenResponse(BaseModel):
    token: str


class IsTokenValidResponse(BaseModel):
    is_valid: bool


class AuthNalogController(Controller):
    path = "/auth-nalog"
    tags = ("Nalog auth",)
    security = security_defs

    @post(
        path="/request",
        description=(
            "Request SMS code for auth at nalog.ru."
        ),
        responses={
            201: success_spec("Requested successfully.", None),
            401: error_spec("Not authenticated."),
            503: error_spec("nalog.ru returned unexpected response.")
        }
    )
    @inject
    async def request_code(
            self, *, interactor: FromDishka[RequestNalogAuthCodeInteractor]
    ) -> None:
        """Login a user."""
        await interactor()

    @post(
        path="/submit",
        description=(
            "Submit SMS code."
        ),
        responses={
            201: success_spec("Successful.", TokenResponse),
            401: error_spec("Not authenticated."),
            503: error_spec("nalog.ru returned unexpected response.")
        }
    )
    @inject
    async def submit_code(
            self, *,
            data: SubmitCodeSchema,
            interactor: FromDishka[SubmitNalogAuthCodeInteractor]
    ) -> TokenResponse:
        token = await interactor(data.code)
        return TokenResponse(token=token)

    @get(
        path="/check",
        description=(
            "Check my nalog.ru access token."
        ),
        responses={
            200: success_spec("Success.", IsTokenValidResponse),
            401: error_spec("Not authenticated."),
            503: error_spec("nalog.ru returned unexpected response.")
        }
    )
    @inject
    async def check_token(
            self, *,
            interactor: FromDishka[CheckNalogAuthTokenInteractor]
    ) -> IsTokenValidResponse:
        is_valid = await interactor()
        return IsTokenValidResponse(is_valid=is_valid)
