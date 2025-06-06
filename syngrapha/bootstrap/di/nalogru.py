from dishka import Provider, Scope, provide

from syngrapha.application.external.nalog import NalogClient
from syngrapha.infrastructure.nalogru.client import NalogClientImpl


class NalogRuDIProvider(Provider):
    """Provides nalog.ru client."""

    client = provide(
        NalogClientImpl,
        provides=NalogClient,
        scope=Scope.APP
    )
