import uuid
from decimal import Decimal
from typing import Collection, cast

from sqlalchemy import select

from syngrapha.application.persistence.transactions import TransactionGateway
from syngrapha.domain.money import Money
from syngrapha.domain.product.category import Category
from syngrapha.domain.product.product import Product, AutoCategorizingState
from syngrapha.domain.transaction.transaction import Transaction
from syngrapha.domain.user import UserId
from syngrapha.infrastructure.persistence.models import ProductModel, TransactionModel
from syngrapha.infrastructure.persistence.uow import SAUoW
from syngrapha.utils.decorator import impl


class TransactionGatewayImpl(TransactionGateway):
    """Impl."""

    uow: SAUoW

    @impl
    async def save_transaction(self, transaction: Transaction) -> None:
        prod_models = [
            ProductModel(
                uuid=prod.id,
                transaction_id=transaction.id,
                name=prod.product,
                price=int((prod.price.as_decimal * 100).to_integral_value()),
                quantity=prod.quantity,
            )
            for prod in transaction.products
        ]
        trans_model = TransactionModel(
            uuid=transaction.id,
            deal_at=transaction.time_of_deal,
            merchant=transaction.merchant,
            user_id=transaction.owner
        )
        self.uow.session.add(trans_model, *prod_models)

    async def get_of_user(self, user_id: UserId) -> Collection[Transaction]:
        t_qry = select(TransactionModel).where(TransactionModel.user_id == user_id)
        result = await self.uow.session.execute(t_qry)
        return [
            Transaction(
                id=cast(uuid.UUID, transaction.uuid),
                owner=cast(uuid.UUID, transaction.user_id),
                merchant=transaction.merchant,
                time_of_deal=transaction.deal_at,
                products=[
                    Product(
                        id=cast(uuid.UUID, product.uuid),
                        product=product.name,
                        quantity=product.quantity,
                        price=Money.from_decimal(
                            Decimal(product.price) / 100,
                            multiplier=100
                        ),
                        category=Category(product.category),
                        auto_cat_state=AutoCategorizingState(product.auto_cat_state),
                    )
                    for product in transaction.products
                ]
            )
            for transaction in result.scalars().all()
        ]
