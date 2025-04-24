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
    reviews: Mapped[list["CarReviewModel"]] = relationship(back_populates="user")


class BanLogModel(Base, IntegerIDMixin):
    __tablename__ = "ban_log"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    reason: Mapped[str] = mapped_column(String(250))
    date_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    date_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped["UserModel"] = relationship(back_populates="bans")


class CarBrand(Base, IntegerIDMixin):
    __tablename__ = "car_brand"

    name: Mapped[str] = mapped_column(String(32))

    cars: Mapped[list["CarModel"]] = relationship(back_populates="car_brand")


class TransmissionModel(Base, IntegerIDMixin):
    __tablename__ = "transmission"

    name: Mapped[str] = mapped_column(String(32))

    cars: Mapped[list["CarModel"]] = relationship(back_populates="transmission")


class CarBodyModel(Base, IntegerIDMixin):
    __tablename__ = "car_body"

    name: Mapped[str] = mapped_column(String(32))

    cars: Mapped[list["CarModel"]] = relationship(back_populates="body")


class EngineTypeModel(Base, IntegerIDMixin):
    # Тип двигателя
    __tablename__ = "engine_type"

    name: Mapped[str] = mapped_column(String(32))

    cars: Mapped[list["CarModel"]] = relationship(back_populates="engine")


class DriveTypeModel(Base, IntegerIDMixin):
    # Тип привода
    __tablename__ = "drive_type"

    name: Mapped[str] = mapped_column(String(32))

    cars: Mapped[list["CarModel"]] = relationship(back_populates="drive")


class CarModel(Base, IntegerIDMixin):
    __tablename__ = "car"

    car_brand_id: Mapped[int] = mapped_column(ForeignKey("car_brand.id", ondelete="CASCADE"))
    model: Mapped[str] = mapped_column(String(32))
    transmission_id: Mapped[int] = mapped_column(ForeignKey("transmission.id", ondelete="CASCADE"))
    body_id: Mapped[int] = mapped_column(ForeignKey("car_body.id", ondelete="CASCADE"))
    year_of_issue: Mapped[int] = mapped_column(DateTime(timezone=True))
    engine_type_id: Mapped[int] = mapped_column(ForeignKey("engine_type.id", ondelete="CASCADE"))
    drive_id: Mapped[int] = mapped_column(ForeignKey("drive_type.id", ondelete="CASCADE"))
    mileage: Mapped[int]
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    car_brand: Mapped["CarBrand"] = relationship(back_populates="cars")
    transmission: Mapped["TransmissionModel"] = relationship(back_populates="cars")
    body: Mapped["CarBodyModel"] = relationship(back_populates="cars")
    engine_type: Mapped["EngineTypeModel"] = relationship(back_populates="cars")
    drive: Mapped["DriveTypeModel"] = relationship(back_populates="cars")
    images: Mapped[list["CarImageModel"]] = relationship(back_populates="car")
    reviews: Mapped[list["CarReviewModel"]] = relationship(back_populates="car")


class CarImageModel(Base, IntegerIDMixin):
    __tablename__ = "car_image"

    image_url: Mapped[str] = mapped_column(String(32))
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))

    car: Mapped["CarModel"] = relationship(back_populates="images")


class CarReviewModel(Base, IntegerIDMixin):
    __tablename__ = "car_review"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"))
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id", ondelete="CASCADE"))
    review_text: Mapped[str]
    image_url: Mapped[str] = mapped_column(String(32))

    user: Mapped["UserModel"] = relationship(back_populates="reviews")
    car: Mapped["CarModel"] = relationship(back_populates="reviews")
