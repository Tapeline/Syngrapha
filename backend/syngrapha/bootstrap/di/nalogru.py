from dishka import Provider, Scope, provide

from syngrapha.application.external.checks import SimpleCheckLoader
from syngrapha.application.external.nalog import NalogClient
from syngrapha.infrastructure.nalogru.client import NalogClientImpl
from syngrapha.infrastructure.proverkachecka.client import \
    ProxiedProverkaChekaClient


class NalogRuDIProvider(Provider):
    """Provides nalog.ru client."""

    client = provide(
        NalogClientImpl,
        provides=NalogClient,
        scope=Scope.APP
    )
    pc_proxy = provide(
        ProxiedProverkaChekaClient,
        provides=SimpleCheckLoader,
        scope=Scope.APP,
    )
