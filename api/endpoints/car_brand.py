from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated, List
from models import CarBrand, UserRoles
from schemas import CarBrandCreateSchema, CarBrandReadSchema, CarBrandUpdateSchema
from .depends.db import get_session
from .depends.auth import current_user
from schemas import UserReadSchema

router = APIRouter(prefix="/car-brands", tags=["Car brands"])


async def check_admin(user: UserReadSchema):
    if user.role != UserRoles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can perform this action"
        )


@router.post("/", response_model=CarBrandReadSchema, status_code=status.HTTP_201_CREATED)
async def create_car_brand(
        data: CarBrandCreateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(CarBrand).where(CarBrand.name == data.name)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Car brand with this name already exists"
        )

    new_brand = CarBrand(**data.model_dump())
    session.add(new_brand)
    await session.commit()
    await session.refresh(new_brand)
    return new_brand


@router.get("/", response_model=List[CarBrandReadSchema])
async def get_all_car_brands(
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(select(CarBrand))
    return result.scalars().all()


@router.get("/{brand_id}", response_model=CarBrandReadSchema)
async def get_car_brand(
        brand_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(
        select(CarBrand).where(CarBrand.id == brand_id)
    )
    brand = result.scalars().first()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car brand not found"
        )
    return brand


@router.patch("/{brand_id}", response_model=CarBrandReadSchema)
async def update_car_brand(
        brand_id: int,
        data: CarBrandUpdateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(CarBrand).where(CarBrand.id == brand_id)
    )
    brand = result.scalars().first()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car brand not found"
        )

    if data.name:
        result = await session.execute(
            select(CarBrand).where(
                CarBrand.name == data.name,
                CarBrand.id != brand_id
            )
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Car brand with this name already exists"
            )

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(brand, key, value)

    await session.commit()
    await session.refresh(brand)
    return brand


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car_brand(
        brand_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(CarBrand).where(CarBrand.id == brand_id)
    )
    brand = result.scalars().first()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car brand not found"
        )

    if brand.cars:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete car brand with associated cars"
        )

    await session.delete(brand)
    await session.commit()
