from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from endpoints.depends.auth import current_user
from schemas import UserReadSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserReadSchema)
async def get_me(user: Annotated[UserReadSchema, Depends(current_user)]):
    return user
