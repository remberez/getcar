# User
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, Field, ConfigDict

from models import UserRoles


class UserReadSchema(schemas.BaseUser[int]):
    phone: str | None = None
    full_name: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    role: UserRoles
    balance: Decimal


class UserCreateSchema(schemas.BaseUserCreate):
    phone: str
    full_name: str


class UserUpdateSchema(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None


class RentalClassBaseSchema(BaseModel):
    name: str


class RentalClassCreateSchema(RentalClassBaseSchema):
    pass


class RentalClassUpdateSchema(BaseModel):
    name: str | None = None


class RentalClassReadSchema(RentalClassBaseSchema):
    id: int

    class Config:
        from_attributes = True


class CarBrandBaseSchema(BaseModel):
    name: str


class CarBrandCreateSchema(CarBrandBaseSchema):
    pass


class CarBrandUpdateSchema(BaseModel):
    name: str | None = None


class CarBrandReadSchema(CarBrandBaseSchema):
    id: int

    class Config:
        from_attributes = True


class TransmissionBaseSchema(BaseModel):
    name: str = Field(max_length=32)


class TransmissionCreateSchema(TransmissionBaseSchema):
    pass


class TransmissionUpdateSchema(BaseModel):
    """Схема для обновления трансмиссии"""
    name: str | None = Field(None, max_length=32)


class TransmissionReadSchema(TransmissionBaseSchema):
    """Схема для чтения данных трансмиссии"""
    id: int

    class Config:
        from_attributes = True


class CarBodyBaseSchema(BaseModel):
    name: str = Field(..., max_length=32)


class CarBodyCreateSchema(CarBodyBaseSchema):
    pass


class CarBodyUpdateSchema(BaseModel):
    name: str | None = Field(None, max_length=32)


class CarBodyReadSchema(CarBodyBaseSchema):
    id: int

    class Config:
        from_attributes = True


class EngineTypeBaseSchema(BaseModel):
    name: str = Field(
        ...,
        max_length=32,
        description="Название типа двигателя"
    )


class EngineTypeCreateSchema(EngineTypeBaseSchema):
    pass


class EngineTypeUpdateSchema(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=32,
        description="Новое название типа двигателя"
    )


class EngineTypeReadSchema(EngineTypeBaseSchema):
    id: int = Field(..., description="Идентификатор типа двигателя")

    class Config:
        from_attributes = True


class DriveTypeBaseSchema(BaseModel):
    name: str = Field(max_length=32, description="Название типа привода")


class DriveTypeReadSchema(DriveTypeBaseSchema):
    id: int = Field(description="Идентификатор типа привода")


class DriveTypeCreateSchema(DriveTypeBaseSchema):
    ...


class DriveTypeUpdateSchema(DriveTypeBaseSchema):
    ...


class CarBaseSchema(BaseModel):
    car_brand_id: int = Field(..., description="ID бренда автомобиля")
    model: str = Field(..., max_length=32, description="Модель автомобиля")
    transmission_id: int = Field(..., description="ID типа трансмиссии")
    body_id: int = Field(..., description="ID типа кузова")
    year_of_issue: datetime = Field(..., description="Год выпуска")
    engine_type_id: int = Field(..., description="ID типа двигателя")
    drive_id: int = Field(..., description="ID типа привода")
    mileage: int = Field(..., ge=0, description="Пробег (км)")
    price: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2, description="Цена аренды в сутки")
    rental_class_id: int = Field(..., description="ID класса аренды")
    number_of_seats: Optional[int] = Field(None, ge=1, le=10, description="Количество мест")
    trunk_volume: Optional[int] = Field(None, ge=0, description="Объем багажника (л)")


class CarCreateSchema(CarBaseSchema):
    pass


class CarUpdateSchema(BaseModel):
    car_brand_id: Optional[int] = Field(None, description="ID бренда автомобиля")
    model: Optional[str] = Field(None, max_length=32, description="Модель автомобиля")
    transmission_id: Optional[int] = Field(None, description="ID типа трансмиссии")
    body_id: Optional[int] = Field(None, description="ID типа кузова")
    year_of_issue: Optional[datetime] = Field(None, description="Год выпуска")
    engine_type_id: Optional[int] = Field(None, description="ID типа двигателя")
    drive_id: Optional[int] = Field(None, description="ID типа привода")
    mileage: Optional[int] = Field(None, ge=0, description="Пробег (км)")
    price: Optional[Decimal] = Field(None, gt=0, max_digits=12, decimal_places=2, description="Цена аренды в сутки")
    rental_class_id: Optional[int] = Field(None, description="ID класса аренды")
    number_of_seats: Optional[int] = Field(None, ge=1, le=10, description="Количество мест")
    trunk_volume: Optional[int] = Field(None, ge=0, description="Объем багажника (л)")


class CarImageBaseSchema(BaseModel):
    image_url: str = Field(..., description="URL изображения")
    car_id: int = Field(..., description="ID автомобиля")


class CarImageCreateSchema(CarImageBaseSchema):
    pass


class CarImageReadSchema(CarImageBaseSchema):
    id: int

    class Config:
        from_attributes = True


class CarReadSchema(CarBaseSchema):
    id: int
    car_brand: CarBrandReadSchema
    transmission: TransmissionReadSchema
    body: CarBodyReadSchema
    engine_type: EngineTypeReadSchema
    drive: DriveTypeReadSchema
    rental_class: RentalClassReadSchema
    images: list[CarImageReadSchema]
    model_config = ConfigDict(from_attributes=True)


class BookingBaseSchema(BaseModel):
    car_id: int
    date_start: datetime
    date_end: datetime


class BookingCreate(BaseModel):
    car_id: int
    date_start: datetime
    date_end: datetime


class BookingUpdate(BaseModel):
    car_id: Optional[int] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None


class BookingRead(BaseModel):
    id: int
    user_id: int | None
    car_id: int | None
    date_start: datetime
    date_end: datetime
    car: CarReadSchema | None = None  # Добавляем вложенную машину

    class Config:
        from_attributes = True
