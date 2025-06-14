import uuid

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Response, delete, get, post
from litestar.datastructures import Cookie
from pydantic import BaseModel

from syngrapha.application.interactors.auth.login import LoginInteractor
from syngrapha.application.interactors.auth.logout import (
    RevokeTokensInteractor,
)
from syngrapha.application.interactors.auth.profile import GetProfileInteractor
from syngrapha.application.interactors.auth.register import RegisterInteractor
from syngrapha.config import SecurityConfig
from syngrapha.presentation.http.framework.openapi import (
    error_spec,
    success_spec,
)
from syngrapha.presentation.http.security import security_defs


class LoginSchema(BaseModel):
    username: str
    password: str


class RegisterSchema(LoginSchema):
    phone: str


class TokenResponse(BaseModel):
    token: str


class RegisterResponse(BaseModel):
    id: uuid.UUID
    username: str


class ProfileResponse(BaseModel):
    id: uuid.UUID
    username: str
    phone: str
    nalog_access_token: str | None


class AuthController(Controller):
    path = "/auth"
    tags = ("Auth",)

    @post(
        path="/login",
        description=(
            "Login and get auth token."
        ),
        responses={
            200: success_spec("Login successful.", TokenResponse),
            404: error_spec("Credentials are invalid."),
        },
        response_cookies=[
            Cookie(
                key="SESSION_ID",
                description="the same auth token as returned by response",
                documentation_only=True,
            )
        ],
    )
    @inject
    async def login(
            self, *,
            data: LoginSchema,
            interactor: FromDishka[LoginInteractor],
            security_config: FromDishka[SecurityConfig],
    ) -> Response[TokenResponse]:
        """Login a user."""
        token = await interactor(data.username, data.password)
        return Response(
            TokenResponse(token=token),
            cookies=[
                Cookie(
                    key="SESSION_ID",
                    value=token,
                    expires=int(
                        security_config.token_lifetime.total_seconds()
                    ),
                    httponly=True,
                    secure=True
                )
            ]
        )

    @post(
        path="/register",
        description=(
            "Register user."
        ),
        responses={
            201: success_spec("Register successful.", RegisterResponse),
            409: error_spec("Such user already exists."),
        }
    )
    @inject
    async def register(
            self, *,
            data: RegisterSchema,
            interactor: FromDishka[RegisterInteractor]
    ) -> RegisterResponse:
        user = await interactor(
            data.username,
            data.phone,
            data.password
        )
        return RegisterResponse(
            id=user.id,
            username=user.username
        )

    @get(
        path="/profile",
        description=(
            "Get my profile."
        ),
        responses={
            200: success_spec("Success.", ProfileResponse),
            401: error_spec("Not authenticated."),
        },
        security=security_defs
    )
    @inject
    async def get_profile(
            self, *,
            interactor: FromDishka[GetProfileInteractor]
    ) -> ProfileResponse:
        user = await interactor()
        return ProfileResponse(
            id=user.id,
            username=user.username,
            phone=user.phone_number,
            nalog_access_token=user.nalog_access_token
        )

    @delete(
        path="/revoke-tokens",
        description=(
            "Revoke all access tokens for me."
        ),
        responses={
            204: success_spec("Success.", None),
            401: error_spec("Not authenticated."),
        },
        security=[{"jwt_auth": []}]
    )
    @inject
    async def revoke_tokens(
            self, *,
            interactor: FromDishka[RevokeTokensInteractor]
    ) -> None:
        await interactor()
