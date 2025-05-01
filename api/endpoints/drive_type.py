from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from endpoints.depends.auth import current_user
from endpoints.depends.db import get_session
from models import UserRoles, DriveTypeModel
from schemas import UserReadSchema, DriveTypeReadSchema, DriveTypeCreateSchema, DriveTypeUpdateSchema

router = APIRouter(prefix="/drive-type", tags=["Drive type"])


async def check_admin(user: UserReadSchema):
    if user.role != UserRoles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can perform this action"
        )


@router.post("/", response_model=DriveTypeReadSchema, status_code=status.HTTP_201_CREATED)
async def create_drive_type(
        data: DriveTypeCreateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(DriveTypeModel).where(DriveTypeModel.name == data.name)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Drive type with this name already exists"
        )

    new_drive_type = DriveTypeModel(**data.model_dump())
    session.add(new_drive_type)
    await session.commit()
    await session.refresh(new_drive_type)
    return new_drive_type


@router.get("/", response_model=list[DriveTypeReadSchema])
async def get_all_drive_types(
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(select(DriveTypeModel))
    return result.scalars().all()


@router.get("/{drive_type_id}", response_model=DriveTypeReadSchema)
async def get_drive_type(
        drive_type_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.execute(
        select(DriveTypeModel).where(DriveTypeModel.id == drive_type_id)
    )
    drive_type = result.scalars().first()
    if not drive_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car drive_type not found"
        )
    return drive_type


@router.patch("/{drive_type_id}", response_model=DriveTypeReadSchema)
async def update_drive_type(
        drive_type_id: int,
        data: DriveTypeUpdateSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(DriveTypeModel).where(DriveTypeModel.id == drive_type_id)
    )
    drive_type = result.scalars().first()
    if not drive_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drive type not found"
        )

    if data.name:
        result = await session.execute(
            select(DriveTypeModel).where(
                DriveTypeModel.name == data.name,
                DriveTypeModel.id != drive_type_id
            )
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Drive type with this name already exists"
            )

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(drive_type, key, value)

    await session.commit()
    await session.refresh(drive_type)
    return drive_type


@router.delete("/{drive_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drive_type(
        drive_type_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[UserReadSchema, Depends(current_user)]
):
    await check_admin(user)

    result = await session.execute(
        select(DriveTypeModel).where(DriveTypeModel.id == drive_type_id)
    )
    drive_type = result.scalars().first()
    if not drive_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car drive type not found"
        )

    if drive_type.cars:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete car brand with associated cars"
        )

    await session.delete(drive_type)
    await session.commit()
