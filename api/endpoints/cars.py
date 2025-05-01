from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated, List, Optional
from decimal import Decimal

from sqlalchemy.orm import selectinload

from models import (
    CarModel, UserRoles, RentalClassModel, DriveTypeModel,
    EngineTypeModel, CarBodyModel, TransmissionModel, CarBrand
)
from schemas import CarCreateSchema, CarReadSchema, CarUpdateSchema, UserReadSchema
from .depends.db import get_session
from .depends.auth import current_user

router = APIRouter(prefix="/cars", tags=["Cars"])


async def check_admin(user: UserReadSchema):
    if user.role != UserRoles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администратор может выполнять это действие"
        )


@router.post(
    "/",
    response_model=CarReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый автомобиль",
    description="Создает новую запись автомобиля. Требуются права администратора."
)
async def create_car(
        car_data: CarCreateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    # Проверка существования связанных сущностей
    related_entities = {
        "car_brand_id": CarBrand,
        "transmission_id": TransmissionModel,
        "body_id": CarBodyModel,
        "engine_type_id": EngineTypeModel,
        "drive_id": DriveTypeModel,
        "rental_class_id": RentalClassModel
    }

    for field, model in related_entities.items():
        result = await session.execute(select(model).where(model.id == getattr(car_data, field)))
        if not result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{model} с указанным ID не существует"
            )

    new_car = CarModel(**car_data.model_dump())
    session.add(new_car)
    await session.commit()
    await session.refresh(new_car)
    return new_car


@router.get(
    "/",
    response_model=List[CarReadSchema],
    summary="Получить список автомобилей",
    description="Возвращает список автомобилей с возможностью фильтрации."
)
async def get_all_cars(
        session: Annotated[AsyncSession, Depends(get_session)],
        brand_id: Optional[int] = Query(None, description="Фильтр по ID бренда"),
        model: Optional[str] = Query(None, description="Фильтр по модели (частичное совпадение)"),
        min_price: Optional[Decimal] = Query(None, description="Минимальная цена аренды"),
        max_price: Optional[Decimal] = Query(None, description="Максимальная цена аренды"),
        limit: int = Query(100, le=1000, description="Лимит записей"),
        offset: int = Query(0, ge=0, description="Смещение")
):
    query = select(CarModel).options(
        selectinload(CarModel.car_brand),
        selectinload(CarModel.transmission),
        selectinload(CarModel.body),
        selectinload(CarModel.engine_type),
        selectinload(CarModel.drive),
        selectinload(CarModel.rental_class),
        selectinload(CarModel.images)
    )

    if brand_id:
        query = query.where(CarModel.car_brand_id == brand_id)
    if model:
        query = query.where(CarModel.model.ilike(f"%{model}%"))
    if min_price:
        query = query.where(CarModel.price >= min_price)
    if max_price:
        query = query.where(CarModel.price <= max_price)

    query = query.limit(limit).offset(offset)

    result = await session.execute(query)
    return result.scalars().all()


@router.get(
    "/{car_id}",
    response_model=CarReadSchema,
    summary="Получить автомобиль по ID",
    description="Возвращает полную информацию об автомобиле."
)
async def get_car(
        car_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(
        select(CarModel).where(CarModel.id == car_id)
        .options(
            selectinload(CarModel.car_brand),
            selectinload(CarModel.transmission),
            selectinload(CarModel.body),
            selectinload(CarModel.engine_type),
            selectinload(CarModel.drive),
            selectinload(CarModel.rental_class),
            selectinload(CarModel.images)
        )
    )
    car = result.scalars().first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автомобиль не найден"
        )
    return car


@router.patch(
    "/{car_id}",
    response_model=CarReadSchema,
    summary="Обновить информацию об автомобиле",
    description="Обновляет информацию об автомобиле. Требуются права администратора."
)
async def update_car(
        car_id: int,
        car_data: CarUpdateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(CarModel).where(CarModel.id == car_id)
    )
    car = result.scalars().first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автомобиль не найден"
        )

    # Проверка существования связанных сущностей при обновлении
    related_entities = {
        "car_brand_id": CarBrand,
        "transmission_id": TransmissionModel,
        "body_id": CarBodyModel,
        "engine_type_id": EngineTypeModel,
        "drive_id": DriveTypeModel,
        "rental_class_id": RentalClassModel
    }

    for field, model in related_entities.items():
        result = await session.execute(select(model).where(model.id == getattr(car_data, field)))
        if not result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{model} с указанным ID не существует"
            )

    # Обновляем только переданные поля
    for key, value in car_data.model_dump(exclude_unset=True).items():
        setattr(car, key, value)

    await session.commit()
    await session.refresh(car)
    return car


@router.delete(
    "/{car_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить автомобиль",
    description="Удаляет автомобиль. Требуются права администратора."
)
async def delete_car(
        car_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(CarModel).where(CarModel.id == car_id)
    )
    car = result.scalars().first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автомобиль не найден"
        )

    if car.bookings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невозможно удалить автомобиль с активными бронированиями"
        )

    await session.delete(car)
    await session.commit()
