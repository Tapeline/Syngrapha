from dishka import Provider, Scope, provide, provide_all

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
from syngrapha.application.persistence.products import ProductGateway
from syngrapha.application.persistence.transactions import TransactionGateway
from syngrapha.infrastructure.persistence.product_gw import ProductGatewayImpl
from syngrapha.infrastructure.persistence.transaction_gw import (
    TransactionGatewayImpl,
)


class TransactionDIProvider(Provider):
    """Provides everything related to transactions."""

    interactors = provide_all(
        GetMyTransactionsInteractor,
        QRImportInteractor,
        GetTransactionInteractor,
        GetProductInteractor,
        # TableImportInteractor,
        scope=Scope.REQUEST,
    )
    transaction_gateway = provide(
        TransactionGatewayImpl,
        provides=TransactionGateway,
        scope=Scope.REQUEST
    )
    product_gateway = provide(
        ProductGatewayImpl,
        provides=ProductGateway,
        scope=Scope.REQUEST
    )
