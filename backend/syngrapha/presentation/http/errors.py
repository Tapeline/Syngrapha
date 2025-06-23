from typing import Final

from syngrapha.application.auth.exceptions import (
    UserAlreadyExists,
    UserCredsNotFound,
    UserNotAuthenticated,
    UserNotFound,
)
from syngrapha.application.external.nalog import (
    NalogReturnedError,
    NalogTokenRequiresReAuth,
)
from syngrapha.application.interactors.auth_nalog.submit_code import (
    InvalidNalogSMSCode,
)
from syngrapha.application.persistence.transactions import (
    ProductNotFound,
    TransactionAccessDenied, TransactionNotFound,
)
from syngrapha.presentation.http.framework.errors import (
    gen_handler_mapping,
    infer_code,
)

handlers: Final = gen_handler_mapping({
    UserAlreadyExists: (409, infer_code),
    UserNotFound: (404, infer_code),
    UserCredsNotFound: (401, infer_code),
    UserNotAuthenticated: (401, infer_code),
    NalogReturnedError: (503, infer_code),
    NalogTokenRequiresReAuth: (401, infer_code),
    InvalidNalogSMSCode: (401, infer_code),
    TransactionNotFound: (404, infer_code),
    ProductNotFound: (404, infer_code),
    TransactionAccessDenied: (403, infer_code)
})

