# Файл: app/routers/car_body.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated, List

from models import CarBodyModel, UserRoles
from schemas import (
    CarBodyCreateSchema,
    CarBodyReadSchema,
    CarBodyUpdateSchema
)
from .depends.db import get_session
from .depends.auth import current_user
from schemas import UserReadSchema

router = APIRouter(prefix="/car-bodies", tags=["Car body"])


async def check_admin(user: UserReadSchema):
    if user.role != UserRoles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администратор может выполнять это действие"
        )


@router.post(
    "/",
    response_model=CarBodyReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый тип кузова",
    description="Создает новую запись типа кузова автомобиля. Требуются права администратора."
)
async def create_car_body(
        car_body_data: CarBodyCreateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    # Проверка на существование кузова с таким именем
    existing_body = await session.execute(
        select(CarBodyModel).where(
            CarBodyModel.name == car_body_data.name
        )
    )
    if existing_body.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Тип кузова с таким названием уже существует"
        )

    new_car_body = CarBodyModel(**car_body_data.model_dump())
    session.add(new_car_body)
    await session.commit()
    await session.refresh(new_car_body)
    return new_car_body


@router.get(
    "/",
    response_model=List[CarBodyReadSchema],
    summary="Получить список всех типов кузовов",
    description="Возвращает список всех доступных типов кузовов автомобилей."
)
async def get_all_car_bodies(
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(select(CarBodyModel))
    return result.scalars().all()


@router.get(
    "/{car_body_id}",
    response_model=CarBodyReadSchema,
    summary="Получить тип кузова по ID",
    description="Возвращает информацию о конкретном типе кузова по его идентификатору."
)
async def get_car_body(
        car_body_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(
        select(CarBodyModel).where(CarBodyModel.id == car_body_id)
    )
    car_body = result.scalars().first()
    if not car_body:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип кузова не найден"
        )
    return car_body


@router.patch(
    "/{car_body_id}",
    response_model=CarBodyReadSchema,
    summary="Обновить тип кузова",
    description="Обновляет информацию о типе кузова. Требуются права администратора."
)
async def update_car_body(
        car_body_id: int,
        car_body_data: CarBodyUpdateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(CarBodyModel).where(CarBodyModel.id == car_body_id)
    )
    car_body = result.scalars().first()
    if not car_body:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип кузова не найден"
        )

    # Проверка на уникальность имени при обновлении
    if car_body_data.name:
        existing_body = await session.execute(
            select(CarBodyModel).where(
                CarBodyModel.name == car_body_data.name,
                CarBodyModel.id != car_body_id
            )
        )
        if existing_body.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Тип кузова с таким названием уже существует"
            )

    # Обновляем только переданные поля
    for key, value in car_body_data.model_dump(exclude_unset=True).items():
        setattr(car_body, key, value)

    await session.commit()
    await session.refresh(car_body)
    return car_body


@router.delete(
    "/{car_body_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить тип кузова",
    description="Удаляет тип кузова. Требуются права администратора. Нельзя удалить тип кузова, связанный с автомобилями."
)
async def delete_car_body(
        car_body_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(CarBodyModel).where(CarBodyModel.id == car_body_id)
    )
    car_body = result.scalars().first()
    if not car_body:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип кузова не найден"
        )

    # Проверка на связанные автомобили
    if car_body.cars:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невозможно удалить тип кузова, так как есть связанные автомобили"
        )

    await session.delete(car_body)
    await session.commit()
