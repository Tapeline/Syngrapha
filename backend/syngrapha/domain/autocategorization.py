import uuid
from dataclasses import dataclass
from typing import final

from syngrapha.domain.product.product import ProductId

type AutoCatProcessId = uuid.UUID


@dataclass(slots=True)
@final
class AutoCategorizationProcess:
    """Autocategorization process domain model."""

    id: AutoCatProcessId
    targets: list[ProductId]
