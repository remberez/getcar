from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from endpoints.depends.auth import current_user
from endpoints.depends.db import get_session
from models import UserModel
from schemas import UserReadSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserReadSchema)
async def get_me(user: Annotated[UserReadSchema, Depends(current_user)]):
    return user


@router.patch("/me", response_model=UserReadSchema)
async def change_me(
    user: Annotated[UserReadSchema, Depends(current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: UserUpdateSchema,
):
    stmt = (
        update(UserModel)
        .where(UserModel.id == user.id)
        .values(**data.model_dump(exclude_none=True))
    )

    print(data)

    await session.execute(stmt)
    await session.commit()

    result = await session.execute(select(UserModel).where(UserModel.id == user.id))
    updated_user = result.scalar_one()

    return updated_user
