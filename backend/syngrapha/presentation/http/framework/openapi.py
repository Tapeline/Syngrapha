from typing import Any

from litestar.openapi import ResponseSpec
from pydantic import BaseModel


class CommonErrorSchema(BaseModel):
    """Used for all errors."""

    code: str
    details: str
    extra: dict[str, Any] | None = None


def success_spec[_Response_T](
        description: str,
        container: type[_Response_T] | None = None
) -> ResponseSpec:
    """Return response spec with success and data."""
    return ResponseSpec(
        description=description,
        data_container=container
    )


def error_spec(description: str) -> ResponseSpec:
    """Return response spec with error schema."""
    return ResponseSpec(
        description=description,
        data_container=CommonErrorSchema,
        generate_examples=False
    )
