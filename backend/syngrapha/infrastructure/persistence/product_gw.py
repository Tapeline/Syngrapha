from collections.abc import Collection
from dataclasses import dataclass
from typing import Mapping

from sqlalchemy import select

from syngrapha.application.persistence.products import ProductGateway
from syngrapha.domain.product.category import Category
from syngrapha.domain.product.product import (
    AutoCategorizingState, ProductId, ProductName,
)
from syngrapha.infrastructure.persistence.models import (
    ProductModel,
)
from syngrapha.infrastructure.persistence.uow import SAUoW


@dataclass(slots=True)
class ProductGatewayImpl(ProductGateway):
    """Impl."""

    uow: SAUoW

    async def get_product_names(
            self, ids: Collection[ProductId]
    ) -> Mapping[ProductId, ProductName]:
        query = select(ProductModel).where(ProductModel.uuid.in_(ids))
        result = await self.uow.session.execute(query)
        return {
            product.uuid: product.name
            for product in result.scalars().all()
        }

    async def save_product_categories(
            self,
            categories: Mapping[ProductId, Category | None]
    ) -> None:
        query = select(ProductModel).where(
            ProductModel.uuid.in_(categories.keys())
        )
        result = await self.uow.session.execute(query)
        for product in result.scalars().all():
            product.category = (
                categories[product.uuid].value
                if categories[product.uuid]
                else None
            )
            product.auto_cat_state = AutoCategorizingState.MARKED.value
            self.uow.session.add(product)
