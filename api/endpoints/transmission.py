# Файл: app/routers/transmission.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated, List

from models import TransmissionModel, UserRoles
from schemas import (
    TransmissionCreateSchema,
    TransmissionReadSchema,
    TransmissionUpdateSchema
)
from .depends.db import get_session
from .depends.auth import current_user
from schemas import UserReadSchema

router = APIRouter(prefix="/transmissions", tags=["Transmissions"])


async def check_admin(user: UserReadSchema):
    """Проверка прав администратора"""
    if user.role != UserRoles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администратор может выполнять это действие"
        )


@router.post(
    "/",
    response_model=TransmissionReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую трансмиссию",
    description="Создает новую запись типа трансмиссии. Требуются права администратора."
)
async def create_transmission(
        transmission_data: TransmissionCreateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    # Проверка на существование трансмиссии с таким именем
    existing_transmission = await session.execute(
        select(TransmissionModel).where(
            TransmissionModel.name == transmission_data.name
        )
    )
    if existing_transmission.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Трансмиссия с таким названием уже существует"
        )

    new_transmission = TransmissionModel(**transmission_data.model_dump())
    session.add(new_transmission)
    await session.commit()
    await session.refresh(new_transmission)
    return new_transmission


@router.get(
    "/",
    response_model=List[TransmissionReadSchema],
    summary="Получить список всех трансмиссий",
    description="Возвращает список всех доступных типов трансмиссий."
)
async def get_all_transmissions(
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(select(TransmissionModel))
    return result.scalars().all()


@router.get(
    "/{transmission_id}",
    response_model=TransmissionReadSchema,
    summary="Получить трансмиссию по ID",
    description="Возвращает информацию о конкретной трансмиссии по её идентификатору."
)
async def get_transmission(
        transmission_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(
        select(TransmissionModel).where(TransmissionModel.id == transmission_id)
    )
    transmission = result.scalars().first()
    if not transmission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Трансмиссия не найдена"
        )
    return transmission


@router.patch(
    "/{transmission_id}",
    response_model=TransmissionReadSchema,
    summary="Обновить трансмиссию",
    description="Обновляет информацию о трансмиссии. Требуются права администратора."
)
async def update_transmission(
        transmission_id: int,
        transmission_data: TransmissionUpdateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(TransmissionModel).where(TransmissionModel.id == transmission_id)
    )
    transmission = result.scalars().first()
    if not transmission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Трансмиссия не найдена"
        )

    # Проверка на уникальность имени при обновлении
    if transmission_data.name:
        existing_transmission = await session.execute(
            select(TransmissionModel).where(
                TransmissionModel.name == transmission_data.name,
                TransmissionModel.id != transmission_id
            )
        )
        if existing_transmission.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Трансмиссия с таким названием уже существует"
            )

    # Обновляем только переданные поля
    for key, value in transmission_data.model_dump(exclude_unset=True).items():
        setattr(transmission, key, value)

    await session.commit()
    await session.refresh(transmission)
    return transmission


@router.delete(
    "/{transmission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить трансмиссию",
    description="Удаляет трансмиссию. Требуются права администратора. Нельзя удалить трансмиссию, связанную с автомобилями."
)
async def delete_transmission(
        transmission_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(TransmissionModel).where(TransmissionModel.id == transmission_id)
    )
    transmission = result.scalars().first()
    if not transmission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Трансмиссия не найдена"
        )

    # Проверка на связанные автомобили
    if transmission.cars:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невозможно удалить трансмиссию, так как есть связанные автомобили"
        )

    await session.delete(transmission)
    await session.commit()
