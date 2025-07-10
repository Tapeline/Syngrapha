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


class NalogConfig(BaseModel):
    """nalog.ru config."""

    secret: str = Field(
        alias="NALOG_SECRET",
        default="IyvrAbKt9h/8p6a7QPh8gpkXYQ4="
        # works for everyone, I reckon
        # was published in some habr.com article
    )


class ProverkaChekaConfig(BaseModel):
    """ProverkaCheka proxy config."""

    base_url: str = Field(alias="PC_PROXY_URL")


class AIConfig(BaseModel):
    """nalog.ru config."""

    key: str = Field(
        alias="AI_KEY",
    )


class Config(BaseModel):
    """Config model."""

    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(**os.environ)  # type: ignore
    )
    security: SecurityConfig = Field(
        default_factory=lambda: SecurityConfig(**os.environ)  # type: ignore
    )
    nalog: NalogConfig = Field(
        default_factory=lambda: NalogConfig(**os.environ)
    )
    ai: AIConfig = Field(
        default_factory=lambda: AIConfig(**os.environ)
    )
    pc_proxy: ProverkaChekaConfig = Field(
        default_factory=lambda: ProverkaChekaConfig(**os.environ)
    )
