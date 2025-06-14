from collections.abc import Collection
from datetime import datetime
from typing import final

from syngrapha.application.auth.auth import UserIdProvider
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.transactions import TransactionGateway
from syngrapha.domain.transaction.transaction import Transaction
from syngrapha.utils.decorator import impl


@interactor
@final
class GetMyTransactionsInteractor:
    """Get all transactions for logged user."""

    user_idp: UserIdProvider
    transaction_gw: TransactionGateway

    @impl
    async def __call__(
            self, since: datetime | None, before: datetime | None
    ) -> Collection[Transaction]:
        user_id = await self.user_idp.get_user()
        return await self.transaction_gw.get_of_user(user_id, since, before)
