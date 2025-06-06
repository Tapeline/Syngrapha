from typing import final

from syngrapha.application.auth.auth import UserIdProvider
from syngrapha.application.external.ai_categorizer import AICategorizerService
from syngrapha.application.identifier import UUIDGenerator
from syngrapha.application.interactors.common import interactor
from syngrapha.application.persistence.transactions import TransactionGateway
from syngrapha.application.persistence.uow import UoW


@interactor
@final
class TableImportInteractor:
    """Import transactions from table."""

    user_idp: UserIdProvider
    transaction_gateway: TransactionGateway
    id_gen: UUIDGenerator
    uow: UoW
    ai_categorizer: AICategorizerService
