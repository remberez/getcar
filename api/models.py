from datetime import datetime
from decimal import Decimal
from enum import Enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable, SQLAlchemyAccessTokenDatabase
from sqlalchemy import DateTime, Enum as SQLEnum, Numeric, ForeignKey, String, Integer, func
from sqlalchemy.ext.asyncio import AsyncSession
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    role: Mapped[UserRoles] = mapped_column(SQLEnum(UserRoles), default=UserRoles.USER)
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default="0.00")

    bans: Mapped[list["BanLogModel"]] = relationship(back_populates="user")
    reviews: Mapped[list["CarReviewModel"]] = relationship(back_populates="user")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)


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

    cars: Mapped[list["CarModel"]] = relationship(back_populates="engine_type")


class DriveTypeModel(Base, IntegerIDMixin):
    # Тип привода
    __tablename__ = "drive_type"

    name: Mapped[str] = mapped_column(String(32))

    cars: Mapped[list["CarModel"]] = relationship(back_populates="drive")


class RentalClassModel(Base, IntegerIDMixin):
    __tablename__ = "rental_class"

    name: Mapped[str] = mapped_column(String(32))

    cars: Mapped[list["CarModel"]] = relationship(back_populates="rental_class")


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
    rental_class_id: Mapped[int] = mapped_column(ForeignKey("rental_class.id"))
    number_of_seats: Mapped[int] = mapped_column(nullable=True)
    trunk_volume: Mapped[int] = mapped_column(nullable=True)

    car_brand: Mapped["CarBrand"] = relationship(back_populates="cars")
    transmission: Mapped["TransmissionModel"] = relationship(back_populates="cars")
    body: Mapped["CarBodyModel"] = relationship(back_populates="cars")
    engine_type: Mapped["EngineTypeModel"] = relationship(back_populates="cars")
    drive: Mapped["DriveTypeModel"] = relationship(back_populates="cars")
    images: Mapped[list["CarImageModel"]] = relationship(back_populates="car")
    reviews: Mapped[list["CarReviewModel"]] = relationship(back_populates="car")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="car")
    rental_class: Mapped["RentalClassModel"] = relationship(back_populates="cars")


class CarImageModel(Base, IntegerIDMixin):
    __tablename__ = "car_image"

    image_url: Mapped[str] = mapped_column(String(128))
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


class Booking(Base, IntegerIDMixin):
    __tablename__ = "booking"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"))
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id", ondelete="SET NULL"))
    date_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    date_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped["UserModel"] = relationship(back_populates="bookings")
    car: Mapped["CarModel"] = relationship(back_populates="bookings")


class AccessTokenModel(Base, SQLAlchemyBaseAccessTokenTable[int]):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="cascade"),
        nullable=True,
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyAccessTokenDatabase(session, cls)
