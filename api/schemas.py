# User
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel

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


class UserUpdateSchema(schemas.BaseUserUpdate):
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
