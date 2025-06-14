import asyncio
import sys

from dishka import AsyncContainer, make_async_container
from dishka.integrations.litestar import LitestarProvider, setup_dishka
from litestar import Litestar
from litestar.logging import LoggingConfig

from syngrapha.bootstrap.di.ai import AICategorizerDIProvider
from syngrapha.bootstrap.di.algorithms import AlgorithmsDIProvider
from syngrapha.bootstrap.di.auth import AuthTokenDIProvider
from syngrapha.bootstrap.di.auth_nalog import AuthNalogDIProvider
from syngrapha.bootstrap.di.config import ConfigDIProvider
from syngrapha.bootstrap.di.nalogru import NalogRuDIProvider
from syngrapha.bootstrap.di.transactions import TransactionDIProvider
from syngrapha.bootstrap.di.uow import UoWDIProvider
from syngrapha.bootstrap.di.user import UserDIProvider
from syngrapha.config import Config
from syngrapha.presentation.http.controllers import route_handlers
from syngrapha.presentation.http.errors import handlers

from syngrapha.presentation.http.openapi import app_openapi_config


def _create_config() -> Config:
    return Config()


def _create_container(config: Config) -> AsyncContainer:
    return make_async_container(
        LitestarProvider(),
        ConfigDIProvider(),
        AlgorithmsDIProvider(),
        UoWDIProvider(),
        UserDIProvider(),
        AuthTokenDIProvider(),
        NalogRuDIProvider(),
        AuthNalogDIProvider(),
        TransactionDIProvider(),
        AICategorizerDIProvider(),
        context={
            Config: config
        },
    )


def _select_event_loop() -> None:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )


def _create_logging_config() -> LoggingConfig:
    return LoggingConfig(
        root={"level": "INFO", "handlers": ["queue_listener"]},
        formatters={
            "standard": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            }
        },
        log_exceptions="always",
    )


def create_app() -> Litestar:
    """Bootstrap the app."""
    _select_event_loop()
    config = _create_config()
    container = _create_container(config)
    logging_config = _create_logging_config()
    litestar_app = Litestar(
        debug=True,
        route_handlers=route_handlers,
        middleware=[],
        exception_handlers=handlers,  # type: ignore
        openapi_config=app_openapi_config,
        logging_config=logging_config,
    )
    setup_dishka(container, litestar_app)
    return litestar_app
