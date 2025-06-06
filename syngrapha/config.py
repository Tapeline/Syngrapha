import os
from datetime import timedelta

from pydantic import BaseModel, Field


class PostgresConfig(BaseModel):
    """Postgres config."""

    host: str = Field(alias="DB_HOST")
    port: int = Field(alias="DB_PORT")
    username: str = Field(alias="DB_USER")
    password: str = Field(alias="DB_PASS")
    database: str = Field(alias="DB_NAME")


class SecurityConfig(BaseModel):
    """Security config."""

    token_lifetime: timedelta = Field(
        alias="SEC_TOK_LIFETIME",
        default=timedelta(hours=48)
    )


class Config(BaseModel):
    """Config model."""

    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(**os.environ)  # type: ignore
    )
    security: SecurityConfig = Field(
        default_factory=lambda: SecurityConfig(**os.environ)  # type: ignore
    )
