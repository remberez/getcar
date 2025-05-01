from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as user_router
from .rental_class import router as rental_router
from .car_brand import router as car_brand_router
from .transmission import router as transmission_router

router = APIRouter(prefix="/api")

router.include_router(router=auth_router)
router.include_router(router=user_router)
router.include_router(router=rental_router)
router.include_router(router=car_brand_router)
router.include_router(router=transmission_router)
