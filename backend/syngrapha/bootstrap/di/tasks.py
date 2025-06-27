from dishka import Provider, Scope, from_context, provide
from taskiq import AsyncBroker, InMemoryBroker
from taskiq_nats import NatsBroker

from syngrapha.application.tasks.ai_tasks import AICategorizeTaskScheduler
from syngrapha.infrastructure.tasks import AICategorizerTaskSchedulerImpl


class TaskDIProvider(Provider):
    """Provides everything related to async tasks."""

    broker = from_context(AsyncBroker, scope=Scope.APP)
    ai_scheduler = provide(
        AICategorizerTaskSchedulerImpl,
        provides=AICategorizeTaskScheduler,
        scope=Scope.APP
    )
