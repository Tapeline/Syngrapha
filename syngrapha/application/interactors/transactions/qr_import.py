from typing import final

from syngrapha.application.auth.auth import UserIdProvider
from syngrapha.application.external.ai_categorizer import AICategorizerService
from syngrapha.application.external.nalog import (
    NalogClient,
    NalogTokenRequiresReAuth,
)
from syngrapha.application.identifier import UUIDGenerator
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.transactions import TransactionGateway
from syngrapha.application.persistence.uow import UoW
from syngrapha.application.persistence.user import UserGateway
from syngrapha.domain.product.product import AutoCategorizingState, Product
from syngrapha.domain.transaction.transaction import Transaction
from syngrapha.utils.decorator import impl


@interactor
@final
class QRImportInteractor:
    """Import transaction from receipt QR code."""

    user_idp: UserIdProvider
    nalog_client: NalogClient
    transaction_gw: TransactionGateway
    id_gen: UUIDGenerator
    uow: UoW
    ai_categorizer: AICategorizerService
    user_gw: UserGateway

    @impl
    async def __call__(self, qr_code: str) -> Transaction:
        user_id = await self.user_idp.get_user()
        async with self.uow:
            user = await self.user_gw.get_by_id(user_id)
            token_valid = await self.nalog_client.check_token_valid(
                user.nalog_access_token
            )
            if not token_valid:
                raise NalogTokenRequiresReAuth
            await self.user_gw.lock(user_id)
            receipt = await self.nalog_client.get_receipt(
                user.nalog_access_token or "", qr_code
            )
            products = [
                Product(
                    id=self.id_gen(),
                    product=rec_item.name,
                    quantity=rec_item.quantity,
                    category=None,
                    price=rec_item.price,
                    auto_cat_state=AutoCategorizingState.IN_PROCESS
                )
                for rec_item in receipt.items
            ]
            transaction = Transaction(
                id=self.id_gen(),
                products=products,
                time_of_deal=receipt.created_at,
                merchant=receipt.merchant,
                owner=user_id
            )
            await self.transaction_gw.save_transaction(transaction)
            await self.ai_categorizer.notify_need_to_categorize(
                {prod.id for prod in products}
            )
            return transaction
