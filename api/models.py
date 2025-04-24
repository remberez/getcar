from datetime import datetime
from decimal import Decimal
from enum import Enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import DateTime, Enum as SQLEnum, Numeric, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class UserRoles(Enum):
    ADMIN = "admin"
    USER = "user"


class Base(DeclarativeBase):
    ...


class IntegerIDMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class UserModel(Base, IntegerIDMixin, SQLAlchemyBaseUserTable[int]):
    phone: Mapped[str]
    full_name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    role: Mapped[UserRoles] = mapped_column(SQLEnum(UserRoles))
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    bans: Mapped[list["BanLogModel"]] = relationship(back_populates="user")


class BanLogModel(Base, IntegerIDMixin):
    __tablename__ = "ban_log"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    reason: Mapped[str] = mapped_column(String(250))
    date_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    date_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped["UserModel"] = relationship(back_populates="bans")
