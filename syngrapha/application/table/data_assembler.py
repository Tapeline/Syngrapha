from dataclasses import dataclass

from syngrapha.application.identifier import UUIDGenerator
from syngrapha.application.table.table import Table
from syngrapha.application.table.transform import money_tf, iso_date_tf
from syngrapha.domain.product.product import Product, AutoCategorizingState
from syngrapha.domain.transaction.transaction import Transaction
from syngrapha.domain.user import UserId
from syngrapha.application.table.exceptions import TableDataTransformerFailed, TableColumnLoadingFailed


# Transformer example: trans_example.json


def assemble_table(data: list[list[str]]) -> Table:
    """
    Try to assemble a table from a list of lists.

    Args:
        data: list of lists -- table.

    Returns: Table

    Raises:
        TableDataTransformerFailed

    """
    try:
        col_names = data[0]
        return Table(col_names, data[1:])
    except Exception as exc:
        raise TableDataTransformerFailed from exc


RegexPattern = str


@dataclass
class DataLoader:
    """Loads data from table."""

    name_col: RegexPattern
    price_col: RegexPattern
    date_col: RegexPattern
    merchant_col: RegexPattern

    def load(
            self, id_gen: UUIDGenerator, user_id: UserId, table: Table
    ) -> list[Transaction]:
        """
        Load transactions from table.

        Args:
            user_id: UserId of the user.
            table: source

        Returns: list of Transactions

        Raises:
            TableColumnLoadingFailed: if columns are not found.
            TableDataTransformerFailed: if data loading failed.

        """
        name_col = table.find_col_by_regex(self.name_col)
        price_col = table.find_col_by_regex(self.price_col)
        date_col = table.find_col_by_regex(self.date_col)
        merchant_col = table.find_col_by_regex(self.merchant_col)
        if not all([name_col, price_col, date_col, merchant_col]):
            raise TableColumnLoadingFailed
        return [
            _load_row(
                row, user_id, id_gen, name_col,
                price_col, date_col, merchant_col
            )
            for row in table.rows
        ]


def _load_row(
        row: list[str],
        user_id: UserId,
        id_gen: UUIDGenerator,
        name_col: int,
        price_col: int,
        date_col: int,
        merchant_col: int
) -> Transaction:
    try:
        name = row[name_col]
        price = money_tf(row[price_col])
        date = iso_date_tf(row[date_col])
        merchant = row[merchant_col]
    except Exception as exc:
        raise TableDataTransformerFailed from exc
    return Transaction(
        id=id_gen(),
        time_of_deal=date,
        merchant=merchant,
        owner=user_id,
        products=[
            Product(
                id=id_gen(),
                product=name,
                price=price,
                quantity=1,
                category=None,
                auto_cat_state=AutoCategorizingState.IN_PROCESS
            )
        ]
    )
