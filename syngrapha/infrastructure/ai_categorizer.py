from collections.abc import Collection

from syngrapha.application.external.ai_categorizer import AICategorizerService
from syngrapha.domain.product.product import ProductId
from syngrapha.utils.decorator import impl


class AICategorizerServiceImpl(AICategorizerService):
    """Impl."""

    @impl
    async def notify_need_to_categorize(
            self,
            ids: Collection[ProductId]
    ) -> None:
        print("Notified", ids)
