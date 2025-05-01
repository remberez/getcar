from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated, List

from models import EngineTypeModel, UserRoles
from schemas import (
    EngineTypeCreateSchema,
    EngineTypeReadSchema,
    EngineTypeUpdateSchema
)
from .depends.db import get_session
from .depends.auth import current_user
from schemas import UserReadSchema

router = APIRouter(prefix="/engine-types", tags=["Engine type"])


async def check_admin(user: UserReadSchema):
    """Проверка прав администратора"""
    if user.role != UserRoles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администратор может выполнять это действие"
        )


@router.post(
    "/",
    response_model=EngineTypeReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый тип двигателя",
    description="Создает новую запись типа двигателя. Требуются права администратора."
)
async def create_engine_type(
        engine_type_data: EngineTypeCreateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    # Проверка на существование типа двигателя с таким именем
    existing_type = await session.execute(
        select(EngineTypeModel).where(
            EngineTypeModel.name == engine_type_data.name
        )
    )
    if existing_type.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Тип двигателя с таким названием уже существует"
        )

    new_engine_type = EngineTypeModel(**engine_type_data.model_dump())
    session.add(new_engine_type)
    await session.commit()
    await session.refresh(new_engine_type)
    return new_engine_type


@router.get(
    "/",
    response_model=List[EngineTypeReadSchema],
    summary="Получить список всех типов двигателей",
    description="Возвращает список всех доступных типов двигателей."
)
async def get_all_engine_types(
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(select(EngineTypeModel))
    return result.scalars().all()


@router.get(
    "/{engine_type_id}",
    response_model=EngineTypeReadSchema,
    summary="Получить тип двигателя по ID",
    description="Возвращает информацию о конкретном типе двигателя по его идентификатору."
)
async def get_engine_type(
        engine_type_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(
        select(EngineTypeModel).where(EngineTypeModel.id == engine_type_id)
    )
    engine_type = result.scalars().first()
    if not engine_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип двигателя не найден"
        )
    return engine_type


@router.patch(
    "/{engine_type_id}",
    response_model=EngineTypeReadSchema,
    summary="Обновить тип двигателя",
    description="Обновляет информацию о типе двигателя. Требуются права администратора."
)
async def update_engine_type(
        engine_type_id: int,
        engine_type_data: EngineTypeUpdateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(EngineTypeModel).where(EngineTypeModel.id == engine_type_id)
    )
    engine_type = result.scalars().first()
    if not engine_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип двигателя не найден"
        )

    # Проверка на уникальность имени при обновлении
    if engine_type_data.name:
        existing_type = await session.execute(
            select(EngineTypeModel).where(
                EngineTypeModel.name == engine_type_data.name,
                EngineTypeModel.id != engine_type_id
            )
        )
        if existing_type.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Тип двигателя с таким названием уже существует"
            )

    # Обновляем только переданные поля
    for key, value in engine_type_data.model_dump(exclude_unset=True).items():
        setattr(engine_type, key, value)

    await session.commit()
    await session.refresh(engine_type)
    return engine_type


@router.delete(
    "/{engine_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить тип двигателя",
    description="Удаляет тип двигателя. Требуются права администратора. Нельзя удалить тип двигателя, связанный с автомобилями."
)
async def delete_engine_type(
        engine_type_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(EngineTypeModel).where(EngineTypeModel.id == engine_type_id)
    )
    engine_type = result.scalars().first()
    if not engine_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип двигателя не найден"
        )

    # Проверка на связанные автомобили
    if engine_type.cars:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невозможно удалить тип двигателя, так как есть связанные автомобили"
        )

    await session.delete(engine_type)
    await session.commit()
