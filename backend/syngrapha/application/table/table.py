import re
from dataclasses import dataclass
from typing import final


@dataclass(slots=True)
@final
class Table:
    """Helper class for manipulating tables."""

    column_names: list[str]
    rows: list[list[str]]

    @property
    def columns(self) -> list[list[str]]:
        """Return transposed table: first index -- columns."""
        return [
            [self.rows[row][col] for row in range(len(self.rows))]
            for col in range(len(self.column_names))
        ]

    def find_col_by_regex(self, regex: str) -> int | None:
        """
        Find a column by regex on its name.

        Args:
            regex: regular expression to match column names.

        Returns:
            column number or None if not found.

        """
        pattern = re.compile(regex)
        for col, col_name in enumerate(self.column_names):
            if pattern.match(col_name):
                return col
        return None
