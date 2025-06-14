import uuid

from syngrapha.application.identifier import UUIDGenerator
from syngrapha.utils.decorator import impl


class UUIDGeneratorImpl(UUIDGenerator):
    """Impl."""

    @impl
    def __call__(self) -> uuid.UUID:
        return uuid.uuid4()
