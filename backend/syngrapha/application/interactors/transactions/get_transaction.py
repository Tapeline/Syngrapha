from collections.abc import Collection
from datetime import datetime
from typing import final

from syngrapha.application.auth.auth import UserIdProvider
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.transactions import (
    TransactionAccessDenied,
    TransactionGateway,
)
from syngrapha.domain.transaction.transaction import Transaction, TransactionId
from syngrapha.utils.decorator import impl


@interactor
@final
class GetTransactionInteractor:
    """Get transaction by id."""

    user_idp: UserIdProvider
    transaction_gw: TransactionGateway

    @impl
    async def __call__(
            self, tid: TransactionId
    ) -> Transaction:
        user_id = await self.user_idp.get_user()
        transaction = await self.transaction_gw.get_by_id(tid)
        if transaction.owner != user_id:
            raise TransactionAccessDenied(transaction.id)
        return transaction
