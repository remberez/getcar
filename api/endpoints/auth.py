from fastapi import APIRouter

from .depends.auth import users, auth_backend
from schemas import UserReadSchema, UserCreateSchema

router = APIRouter(prefix="/auth",tags=["Auth"],)

# login, logout
router.include_router(router=users.get_auth_router(auth_backend))

# register
router.include_router(router=users.get_register_router(UserReadSchema, UserCreateSchema))

router.include_router(router=users.get_verify_router(UserReadSchema))
