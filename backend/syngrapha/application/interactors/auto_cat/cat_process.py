from collections.abc import Collection
from typing import final

from syngrapha.application.external.ai_categorizer import AICategorizerService
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.products import ProductGateway
from syngrapha.application.persistence.uow import UoW
from syngrapha.domain.product.product import ProductId


@interactor
@final
class AutoCategorizeInteractor:
    product_gw: ProductGateway
    ai_categorizer: AICategorizerService
    uow: UoW

    async def __call__(self, ids: Collection[ProductId]) -> None:
        products = await self.product_gw.get_product_names(ids)
        print("Now categorizing")
        categories = await self.ai_categorizer.categorize(products)
        async with self.uow:
            await self.product_gw.save_product_categories(categories)
