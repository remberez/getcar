from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated, List
import uuid
import os

from models import CarImageModel, CarModel, UserRoles
from schemas import CarImageReadSchema, UserReadSchema
from .depends.db import get_session
from .depends.auth import current_user
from config import settings

router = APIRouter(prefix="/car-images", tags=["car_images"])


async def check_admin(user: UserReadSchema):
    if user.role != UserRoles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администратор может выполнять это действие"
        )


@router.post(
    "/",
    response_model=CarImageReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить изображение автомобиля",
    description="Загружает новое изображение для автомобиля. Требуются права администратора."
)
async def create_car_image(
        car_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)],
        file: UploadFile = File(...),
):
    await check_admin(user)

    # Проверка существования автомобиля
    car_result = await session.execute(
        select(CarModel).where(CarModel.id == car_id)
    )
    if not car_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автомобиль не найден"
        )

    # Генерация уникального имени файла
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{str(uuid.uuid4())[:25]}{file_ext}"
    file_path = os.path.join(settings.media_root, "car_images", filename)

    # Сохранение файла
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Создание записи в БД
    image_url = f"/media/car_images/{filename}"
    new_image = CarImageModel(
        image_url=image_url,
        car_id=car_id
    )
    session.add(new_image)
    await session.commit()
    await session.refresh(new_image)
    return new_image


@router.get(
    "/car/{car_id}",
    response_model=List[CarImageReadSchema],
    summary="Получить изображения автомобиля",
    description="Возвращает список всех изображений для указанного автомобиля."
)
async def get_car_images(
        car_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    # Проверка существования автомобиля
    car_result = await session.execute(
        select(CarModel).where(CarModel.id == car_id)
    )
    if not car_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автомобиль не найден"
        )

    result = await session.execute(
        select(CarImageModel).where(CarImageModel.car_id == car_id)
    )
    return result.scalars().all()


@router.get(
    "/{image_id}",
    response_model=CarImageReadSchema,
    summary="Получить изображение по ID",
    description="Возвращает информацию об изображении по его идентификатору."
)
async def get_car_image(
        image_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(
        select(CarImageModel).where(CarImageModel.id == image_id)
    )
    image = result.scalars().first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Изображение не найдено"
        )
    return image


@router.delete(
    "/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить изображение",
    description="Удаляет изображение автомобиля. Требуются права администратора."
)
async def delete_car_image(
        image_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(CarImageModel).where(CarImageModel.id == image_id)
    )
    image = result.scalars().first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Изображение не найдено"
        )

    # Удаление файла
    file_path = os.path.join(settings.media_root, image.image_url.replace("/media/", ""))
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении файла: {str(e)}"
        )

    await session.delete(image)
    await session.commit()
