from collections.abc import Collection
from typing import final

from syngrapha.application.interactors.common import interactor
from syngrapha.domain.product.product import ProductId


@interactor
@final
class AutoCategorize:

    async def __call__(self, ids: Collection[ProductId]) -> None:
