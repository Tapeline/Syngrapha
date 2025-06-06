from typing import Final

from syngrapha.application.auth.exceptions import (
    UserAlreadyExists,
    UserCredsNotFound,
    UserNotAuthenticated,
    UserNotFound,
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
})
