import uuid
from collections.abc import Collection
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import cast

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from syngrapha.application.persistence.transactions import (
    TransactionGateway,
    TransactionNotFound,
)
from syngrapha.domain.money import Money
from syngrapha.domain.product.category import Category
from syngrapha.domain.product.product import AutoCategorizingState, Product
from syngrapha.domain.transaction.transaction import Transaction, TransactionId
from syngrapha.domain.user import UserId
from syngrapha.infrastructure.persistence.models import (
    ProductModel,
    TransactionModel,
)
from syngrapha.infrastructure.persistence.uow import SAUoW
from syngrapha.utils.decorator import impl


@dataclass(slots=True)
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
                auto_cat_state=prod.auto_cat_state.value,
                category=(
                    prod.category.value
                    if prod.category
                    else None
                )
            )
            for prod in transaction.products
        ]
        trans_model = TransactionModel(
            uuid=transaction.id,
            deal_at=transaction.time_of_deal,
            merchant=transaction.merchant,
            user_id=transaction.owner
        )
        self.uow.session.add_all([*prod_models, trans_model])

    @impl
    async def get_of_user(
            self, user_id: UserId,
            since: datetime | None = None,
            before: datetime | None = None
    ) -> Collection[Transaction]:
        t_qry = (
            select(TransactionModel)
            .options(selectinload(TransactionModel.products))
            .where(TransactionModel.user_id == user_id)
        )
        if since:
            t_qry = t_qry.where(TransactionModel.deal_at >= since)
        if before:
            t_qry = t_qry.where(TransactionModel.deal_at <= before)
        result = await self.uow.session.execute(t_qry)
        return [
            _transaction_model_to_dm(transaction)
            for transaction in result.scalars().all()
        ]

    async def get_by_id(self, tid: TransactionId) -> Transaction:
        query = (
            select(TransactionModel)
            .options(selectinload(TransactionModel.products))
            .where(TransactionModel.uuid == tid)
        )
        result = await self.uow.session.execute(query)
        transaction = result.scalar_one_or_none()
        if not transaction:
            raise TransactionNotFound(tid)
        return _transaction_model_to_dm(transaction)


def _transaction_model_to_dm(transaction: TransactionModel) -> Transaction:
    return Transaction(
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
                category=(
                    Category(product.category)
                    if product.category
                    else None
                ),
                auto_cat_state=AutoCategorizingState(
                    product.auto_cat_state
                ),
            )
            for product in transaction.products
        ]
    )
