import asyncio
import sys

from dishka import AsyncContainer, make_async_container
from dishka.integrations.litestar import LitestarProvider, setup_dishka
from litestar import Litestar
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from syngrapha.bootstrap.di.algorithms import AlgorithmsDIProvider
from syngrapha.bootstrap.di.auth import HeaderTokenDIProvider
from syngrapha.bootstrap.di.config import ConfigDIProvider
from syngrapha.bootstrap.di.uow import UoWDIProvider
from syngrapha.bootstrap.di.user import UserDIProvider
from syngrapha.config import Config
from syngrapha.presentation.http.errors import handlers
from syngrapha.presentation.http.user import AuthController


def _create_config() -> Config:
    return Config()


def _create_container(config: Config) -> AsyncContainer:
    return make_async_container(
        LitestarProvider(),
        ConfigDIProvider(),
        AlgorithmsDIProvider(),
        UoWDIProvider(),
        UserDIProvider(),
        HeaderTokenDIProvider(),
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
        route_handlers=[
            AuthController,
        ],
        middleware=[],
        exception_handlers=handlers,  # type: ignore
        openapi_config=OpenAPIConfig(
            title="Syngrapha",
            description="Syngrapha API",
            version="1.0.0",
            render_plugins=[
                SwaggerRenderPlugin(),
            ],
            path="/docs",
        ),
        logging_config=logging_config,
    )
    setup_dishka(container, litestar_app)
    return litestar_app
