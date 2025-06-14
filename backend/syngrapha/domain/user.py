import uuid
from dataclasses import dataclass
from typing import final

type UserId = uuid.UUID
type Username = str
type PhoneNumber = str
type NalogToken = str


@dataclass(slots=True)
@final
class User:
    """Defines user domain model."""

    id: UserId
    username: str
    phone_number: PhoneNumber
    nalog_access_token: NalogToken | None
