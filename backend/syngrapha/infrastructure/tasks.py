import asyncio
from dataclasses import dataclass
from typing import Collection
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask

from syngrapha.application.interactors.auto_cat.cat_process import \
    AutoCategorizeInteractor
from syngrapha.application.tasks.ai_tasks import AICategorizeTaskScheduler
from syngrapha.domain.product.product import ProductId
from syngrapha.utils.decorator import impl


class AICategorizerTaskSchedulerImpl(AICategorizeTaskScheduler):
    """Impl."""

    def __init__(self, broker: AsyncBroker) -> None:
        """Create scheduler and init task."""
        self.broker = broker
        self.task: (
            AsyncTaskiqDecoratedTask[[Collection[ProductId]], None]
        ) = self.broker.register_task(  # type: ignore
            _ai_cat_task,
            task_name="ai_cat_task"
        )

    @impl
    async def schedule(self, ids: Collection[ProductId]) -> None:
        print("Task kiqed for", ids)
        await self.task.kiq(list(ids))


@inject(patch_module=True)
async def _ai_cat_task(
        ids: list[UUID], *,
        interactor: FromDishka[AutoCategorizeInteractor]
) -> None:
    await asyncio.sleep(20)
    await interactor(ids)
