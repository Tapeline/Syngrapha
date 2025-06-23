from collections.abc import Collection
from dataclasses import dataclass

from sqlalchemy import update

from syngrapha.application.external.ai_categorizer import AICategorizerService
from syngrapha.application.identifier import UUIDGenerator
from syngrapha.domain.product.category import Category
from syngrapha.domain.product.product import (
    AutoCategorizingState,
    Product,
    ProductId,
)
from syngrapha.infrastructure.ddg_client import DuckDuckGoAI
from syngrapha.infrastructure.persistence.models import ProductModel
from syngrapha.infrastructure.persistence.uow import SAUoW
from syngrapha.utils.decorator import impl


_BASE_PROMPT = (
    f"Дан список товаров из чека. Определи категорию каждого товара. "
    f"Возможные категории: {', '.join(Category)}. "
    f"Отвечай списком из категорий, сохраняя порядок. "
    f"Для каждого товара категория должна быть размещена на отдельной строке "
    f"без каких либо знаков препинания. Категория обязательно должна быть в "
    f"приведенном выше списке. Вот список покупок: \n"
)


@dataclass(frozen=True, slots=True)
class AIClient:
    client: DuckDuckGoAI

    async def request(self, prompt: str) -> str | None:
        await self.client.connect()
        try:
            return await self.client.chat(prompt)
        except Exception:
            return None

    async def _categorize(self, products: list[Product]) -> dict[ProductId, Category]:
        prompt = _BASE_PROMPT + ",\n".join(
            str(product.product) for product in products
        )
        ids = (product.id for product in products)
        response = await self.request(prompt)
        if not response:
            return {}
        cat_names = (
            cat_name.strip(",; .1234567890").upper()
            for cat_name in response.split("\n")
        )
        categories = (
            Category(cat_name)
            if cat_name in Category._value2member_map_
            else None
            for cat_name in cat_names
        )
        return {
            k: v for k, v in zip(ids, categories)
        }


@dataclass(frozen=True, slots=True)
class AICategorizerServiceImpl(AICategorizerService):
    """Impl."""

    uow: SAUoW
    uuid_gen: UUIDGenerator
    ai_client: AIClient

    @impl
    async def notify_need_to_categorize(
            self,
            ids: Collection[ProductId]
    ) -> None:
        upd_qry = update(ProductModel).where(
            ProductModel.uuid.in_(ids)
        ).values(auto_cat_state=AutoCategorizingState.IN_PROCESS)
        await self.uow.session.execute(upd_qry)


async def _categorize(ids: list[Product]):