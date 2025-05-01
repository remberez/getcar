from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as user_router

router = APIRouter(prefix="/api")

router.include_router(router=auth_router)
router.include_router(router=user_router)
