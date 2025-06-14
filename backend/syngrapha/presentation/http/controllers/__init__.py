from typing import Final

from syngrapha.presentation.http.controllers.nalog import AuthNalogController
from syngrapha.presentation.http.controllers.transactions import (
    TransactionsController,
)
from syngrapha.presentation.http.controllers.user import AuthController

route_handlers: Final = (
    AuthController,
    AuthNalogController,
    TransactionsController,
)
