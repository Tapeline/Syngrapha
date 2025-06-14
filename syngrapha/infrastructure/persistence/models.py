from datetime import datetime
from typing import List, final

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import current_timestamp


class Base(DeclarativeBase):
    """Base model."""


@final
class UserModel(Base):
    """Table for users."""

    __tablename__ = "users"

    uuid: Mapped[str] = mapped_column(
        "uuid",
        Uuid,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(
        "username",
        String(length=64),
        unique=True
    )
    hashed_pass: Mapped[str]
    phone_number: Mapped[str]
    nalog_access_token: Mapped[str | None] = mapped_column(
        "nalog_access_token",
        String(256),
        nullable=True
    )


@final
class UserAuthTokenModel(Base):
    """Table for auth tokens."""

    __tablename__ = "tokens"

    user_id: Mapped[str] = mapped_column(
        "user_id",
        ForeignKey("users.uuid")
    )
    user: Mapped[UserModel] = relationship()
    token: Mapped[str] = mapped_column(
        "token",
        String(256),
        primary_key=True
    )
    issued_at: Mapped[datetime] = mapped_column(
        "issued_at",
        DateTime,
        default=datetime.now,
        server_default=current_timestamp()
    )


@final
class TransactionModel(Base):
    """Table for transactions."""

    __tablename__ = "transactions"

    uuid: Mapped[str] = mapped_column(
        "uuid",
        Uuid,
        primary_key=True,
    )
    user_id: Mapped[str] = mapped_column(
        "user_id",
        ForeignKey("users.uuid")
    )
    user: Mapped[UserModel] = relationship()
    deal_at: Mapped[datetime]
    merchant: Mapped[str]
    products: Mapped[List["ProductModel"]] = relationship(
        back_populates="transaction", lazy="selectin"
    )


@final
class ProductModel(Base):
    """Table for product entries."""

    __tablename__ = "products"

    uuid: Mapped[str] = mapped_column(
        "uuid",
        Uuid,
        primary_key=True,
    )
    transaction_id: Mapped[str] = mapped_column(
        "transaction_id",
        ForeignKey("transactions.uuid")
    )
    transaction: Mapped[TransactionModel] = relationship(
        TransactionModel, back_populates="products"
    )
    name: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[float]
    category: Mapped[str | None] = mapped_column(
        "category",
        nullable=True
    )
    auto_cat_state: Mapped[str]
