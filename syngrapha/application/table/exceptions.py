class TableException(Exception):
    """Base exc for tables."""


class TableAssemblyFailed(TableException):
    """Raised when table assembly failed."""


class TableColumnLoadingFailed(TableException):
    """Raised when table column loading failed."""


class TableDataTransformerFailed(TableException):
    """Raised when table data transformer failed."""
