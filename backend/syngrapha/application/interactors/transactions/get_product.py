from typing import final

from syngrapha.application.auth.auth import UserIdProvider
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.transactions import (
    ProductNotFound, TransactionAccessDenied,
    TransactionGateway,
)
from syngrapha.domain.transaction.transaction import (
    Transaction, TransactionId
)
from syngrapha.domain.product.product import Product, ProductId
from syngrapha.utils.decorator import impl


@interactor
@final
class GetProductInteractor:
    """Get transaction's product by id."""

    user_idp: UserIdProvider
    transaction_gw: TransactionGateway

    @impl
    async def __call__(
            self, tid: TransactionId, pid: ProductId
    ) -> Product:
        user_id = await self.user_idp.get_user()
        transaction = await self.transaction_gw.get_by_id(tid)
        if transaction.owner != user_id:
            raise TransactionAccessDenied(transaction.id)
        for product in transaction.products:
            if product.id == pid:
                return product
        raise ProductNotFound(tid, pid)
