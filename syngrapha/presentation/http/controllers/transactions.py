import uuid
from datetime import datetime

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post
from pydantic import BaseModel

from syngrapha.application.interactors.transactions.get_transactions import \
    GetMyTransactionsInteractor
from syngrapha.application.interactors.transactions.qr_import import \
    QRImportInteractor
from syngrapha.domain.transaction.transaction import Transaction
from syngrapha.presentation.http.framework.openapi import (
    error_spec,
    success_spec,
)
from syngrapha.presentation.http.security import security_defs


class QRImportSchema(BaseModel):
    code: str


class ProductResponse(BaseModel):
    id: uuid.UUID
    transaction: uuid.UUID
    name: str
    quantity: float
    price: int
    cost: int
    category: str | None


class TransactionResponse(BaseModel):
    id: uuid.UUID
    merchant: str
    time: datetime
    cost: int
    products: list[ProductResponse]


def _transaction_to_response(transaction: Transaction) -> TransactionResponse:
    return TransactionResponse(
        id=transaction.id,
        merchant=transaction.merchant,
        time=transaction.time_of_deal,
        cost=transaction.cost.as_x100_int,
        products=[
            ProductResponse(
                id=product.id,
                transaction=transaction.id,
                name=product.product,
                quantity=product.quantity,
                price=product.price.as_x100_int,
                cost=product.cost.as_x100_int,
                category=(
                    product.category.value
                    if product.category
                    else None
                )
            )
            for product in transaction.products
        ]
    )


class TransactionsController(Controller):
    path = "/transactions"
    tags = ("Transactions",)
    security = security_defs

    @post(
        path="/import-qr",
        description=(
            "Import from nalog.ru compatible QR code."
        ),
        responses={
            201: success_spec("Imported successfully.", None),
            401: error_spec("Not authenticated."),
            503: error_spec("nalog.ru returned unexpected response.")
        }
    )
    @inject
    async def qr_import(
            self, *,
            data: QRImportSchema,
            interactor: FromDishka[QRImportInteractor]
    ) -> TransactionResponse:
        """Login a user."""
        imported = await interactor(data.code)
        return _transaction_to_response(imported)

    @get(
        path="/my",
        description=(
            "Get my transactions."
        ),
        responses={
            200: success_spec("Successful.", list[TransactionResponse]),
            401: error_spec("Not authenticated."),
        }
    )
    @inject
    async def get_my_transactions(
            self, *,
            interactor: FromDishka[GetMyTransactionsInteractor]
    ) -> list[TransactionResponse]:
        transactions = await interactor(None, None)
        return [
            _transaction_to_response(transaction)
            for transaction in transactions
        ]
