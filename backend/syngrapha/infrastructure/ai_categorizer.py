from dataclasses import dataclass
from typing import Mapping

from syngrapha.application.external.ai_categorizer import AICategorizerService
from syngrapha.config import AIConfig
from syngrapha.domain.product.category import Category
from syngrapha.domain.product.product import (
    ProductId, ProductName,
)
from syngrapha.infrastructure.ai_client import OpenRouterAI


_BASE_PROMPT = (
    f"Дан список товаров из чека. Определи категорию каждого товара. "
    f"Возможные категории: {', '.join(Category)}. "
    f"Отвечай списком из категорий, сохраняя порядок. "
    f"Для каждого товара категория должна быть размещена на отдельной строке "
    f"без каких либо знаков препинания. Категория обязательно должна быть в "
    f"приведенном выше списке. Вот список покупок: \n"
)


class AICategorizerServiceImpl(AICategorizerService):
    def __init__(self, config: AIConfig) -> None:
        """Create client."""
        self.client = OpenRouterAI(config)

    async def request(self, prompt: str) -> str | None:
        try:
            return await self.client.request(prompt)
        except Exception:
            return None

    async def categorize(
            self, products: Mapping[ProductId, ProductName]
    ) -> Mapping[ProductId, Category]:
        ids = list(products.keys())
        names = [products[pid] for pid in ids]
        prompt = _BASE_PROMPT + ",\n".join(names)
        print("Requesting")
        print("===")
        print(prompt)
        response = await self.request(prompt)
        if not response:
            return {}
        print("Responded", response)
        cat_names = (
            cat_name.strip(",; .1234567890").lower()
            for cat_name in response.split("\n")
        )
        categories = (
            Category(cat_name)
            if cat_name in Category._value2member_map_
            else None
            for cat_name in cat_names
        )
        print(categories)
        return {
            k: v for k, v in zip(ids, categories)
        }
