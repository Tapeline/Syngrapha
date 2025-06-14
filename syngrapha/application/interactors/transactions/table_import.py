from typing import final

from syngrapha.application.auth.auth import UserIdProvider
from syngrapha.application.external.ai_categorizer import AICategorizerService
from syngrapha.application.identifier import UUIDGenerator
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.transactions import TransactionGateway
from syngrapha.application.persistence.uow import UoW
from syngrapha.application.persistence.user import UserGateway
from syngrapha.application.table.data_assembler import assemble_table, DataLoader
from syngrapha.domain.transaction.transaction import deduplicate_transactions
from syngrapha.utils.decorator import impl


@interactor
@final
class TableImportInteractor:
    """Import transactions from table."""

    user_idp: UserIdProvider
    user_gw: UserGateway
    transaction_gw: TransactionGateway
    id_gen: UUIDGenerator
    uow: UoW
    ai_categorizer: AICategorizerService

    @impl
    async def __call__(
            self,
            table_repr: list[list[str]],
            loader: DataLoader,
    ) -> None:
        user_id = await self.user_idp.get_user()
        async with self.uow:
            await self.user_gw.lock(user_id)
            table = assemble_table(table_repr)
            new_transactions = loader.load(self.id_gen, user_id, table)
            existing_transactions = await (
                self.transaction_gw.get_of_user(user_id)
            )
            merged_transactions = deduplicate_transactions(
                existing_transactions, new_transactions
            )
            for transaction in merged_transactions:
                await self.transaction_gw.save_transaction(transaction)
