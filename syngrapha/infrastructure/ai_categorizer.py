from typing import Collection

from syngrapha.application.external.ai_categorizer import AICategorizerService
from syngrapha.domain.product.product import ProductId


class AICategorizerServiceImpl(AICategorizerService):
    async def notify_need_to_categorize(
            self,
            ids: Collection[ProductId]
    ) -> None:
        print("Notified", ids)
