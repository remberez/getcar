from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated, List
from models import RentalClassModel, UserRoles
from schemas import RentalClassCreateSchema, RentalClassReadSchema, RentalClassUpdateSchema
from .depends.db import get_session
from .depends.auth import current_user
from schemas import UserReadSchema

router = APIRouter(prefix="/rental-classes", tags=["Rental Classes"])


async def check_admin(user: UserReadSchema):
    if user.role != UserRoles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can perform this action"
        )


@router.post("/", response_model=RentalClassReadSchema, status_code=status.HTTP_201_CREATED)
async def create_rental_class(
        rental_class_data: RentalClassCreateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(RentalClassModel).where(RentalClassModel.name == rental_class_data.name)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rental class with this name already exists"
        )

    new_rental_class = RentalClassModel(**rental_class_data.model_dump())
    session.add(new_rental_class)
    await session.commit()
    await session.refresh(new_rental_class)
    return new_rental_class


@router.get("/", response_model=List[RentalClassReadSchema])
async def get_all_rental_classes(
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(select(RentalClassModel))
    return result.scalars().all()


@router.get("/{rental_class_id}", response_model=RentalClassReadSchema)
async def get_rental_class(
        rental_class_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(
        select(RentalClassModel).where(RentalClassModel.id == rental_class_id)
    )
    rental_class = result.scalars().first()
    if not rental_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental class not found"
        )
    return rental_class


@router.patch("/{rental_class_id}", response_model=RentalClassReadSchema)
async def update_rental_class(
        rental_class_id: int,
        rental_class_data: RentalClassUpdateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(RentalClassModel).where(RentalClassModel.id == rental_class_id)
    )
    rental_class = result.scalars().first()
    if not rental_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental class not found"
        )

    if rental_class_data.name:
        result = await session.execute(
            select(RentalClassModel).where(
                RentalClassModel.name == rental_class_data.name,
                RentalClassModel.id != rental_class_id
            )
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rental class with this name already exists"
            )

    for key, value in rental_class_data.model_dump(exclude_unset=True).items():
        setattr(rental_class, key, value)

    await session.commit()
    await session.refresh(rental_class)
    return rental_class


@router.delete("/{rental_class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rental_class(
        rental_class_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(RentalClassModel).where(RentalClassModel.id == rental_class_id)
    )
    rental_class = result.scalars().first()
    if not rental_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental class not found"
        )

    if rental_class.cars:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete rental class with associated cars"
        )

    await session.delete(rental_class)
    await session.commit()