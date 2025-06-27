import uuid
from datetime import datetime
from typing import cast

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post
from pydantic import BaseModel

from syngrapha.application.interactors.transactions.get_product import \
    GetProductInteractor
from syngrapha.application.interactors.transactions.get_transaction import \
    GetTransactionInteractor
from syngrapha.application.interactors.transactions.get_transactions import (
    GetMyTransactionsInteractor,
)
from syngrapha.application.interactors.transactions.qr_import import (
    QRImportInteractor,
)
from syngrapha.domain.product.product import AutoCategorizingState, Product
from syngrapha.domain.transaction.transaction import Transaction, TransactionId
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
    under_ai_process: bool


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
            _product_to_response(transaction.id, product)
            for product in transaction.products
        ]
    )


def _product_to_response(
        transaction_id: TransactionId, product: Product
) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        transaction=transaction_id,
        name=product.product,
        quantity=product.quantity,
        price=product.price.as_x100_int,
        cost=product.cost.as_x100_int,
        category=(
            product.category.value
            if product.category
            else None
        ),
        under_ai_process=(
            product.auto_cat_state == AutoCategorizingState.IN_PROCESS
        )
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
            since: datetime | None = None,
            before: datetime | None = None,
            interactor: FromDishka[GetMyTransactionsInteractor]
    ) -> list[TransactionResponse]:
        transactions = await interactor(since, before)
        return [
            _transaction_to_response(transaction)
            for transaction in transactions
        ]

    @get(
        path="/{transaction_id:uuid}",
        description=(
                "Get a single transaction."
        ),
        responses={
            200: success_spec("Successful.", TransactionResponse),
            404: error_spec("Not found."),
            403: error_spec("Not permitted."),
            401: error_spec("Not authenticated."),
        }
    )
    @inject
    async def get_transaction(
            self, *,
            transaction_id: uuid.UUID,
            interactor: FromDishka[GetTransactionInteractor]
    ) -> TransactionResponse:
        transaction = await interactor(transaction_id)
        return _transaction_to_response(transaction)

    @get(
        path="/{transaction_id:uuid}/{product_id:uuid}",
        description=(
                "Get a single product in transaction."
        ),
        responses={
            200: success_spec("Successful.", ProductResponse),
            404: error_spec("Not found."),
            403: error_spec("Not permitted."),
            401: error_spec("Not authenticated."),
        }
    )
    @inject
    async def get_product(
            self, *,
            transaction_id: uuid.UUID,
            product_id: uuid.UUID,
            interactor: FromDishka[GetProductInteractor]
    ) -> ProductResponse:
        product = await interactor(transaction_id, product_id)
        return _product_to_response(transaction_id, product)
