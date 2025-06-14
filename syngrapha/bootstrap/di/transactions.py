from dishka import Provider, Scope, provide, provide_all

from syngrapha.application.auth.auth import UserCredentialStore
from syngrapha.application.interactors.auth.login import LoginInteractor
from syngrapha.application.interactors.auth.logout import \
    RevokeTokensInteractor
from syngrapha.application.interactors.auth.profile import GetProfileInteractor
from syngrapha.application.interactors.auth.register import RegisterInteractor
from syngrapha.application.interactors.transactions.get_transactions import \
    GetMyTransactionsInteractor
from syngrapha.application.interactors.transactions.qr_import import \
    QRImportInteractor
from syngrapha.application.interactors.transactions.table_import import \
    TableImportInteractor
from syngrapha.application.persistence.transactions import TransactionGateway
from syngrapha.application.persistence.user import UserGateway
from syngrapha.infrastructure.persistence.auth import UserCredentialStoreImpl
from syngrapha.infrastructure.persistence.transaction_gw import \
    TransactionGatewayImpl
from syngrapha.infrastructure.persistence.user_gw import UserGatewayImpl


class TransactionDIProvider(Provider):
    """Provides everything related to transactions."""

    interactors = provide_all(
        GetMyTransactionsInteractor,
        QRImportInteractor,
        # TableImportInteractor,
        scope=Scope.REQUEST,
    )
    transaction_gateway = provide(
        TransactionGatewayImpl,
        provides=TransactionGateway,
        scope=Scope.REQUEST
    )
