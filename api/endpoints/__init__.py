from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as user_router
from .rental_class import router as rental_router
from .car_brand import router as car_brand_router
from .transmission import router as transmission_router
from .car_body import router as car_body_router
from .engine_type import router as engine_type_router
from .drive_type import router as drive_type_router
from .cars import router as car_router
from .car_images import router as car_images_router
from .booking import router as booking_router

router = APIRouter(prefix="/api")

router.include_router(router=auth_router)
router.include_router(router=user_router)
router.include_router(router=rental_router)
router.include_router(router=car_brand_router)
router.include_router(router=transmission_router)
router.include_router(router=car_body_router)
router.include_router(router=engine_type_router)
router.include_router(router=drive_type_router)
router.include_router(router=car_router)
router.include_router(router=car_images_router)
router.include_router(router=booking_router)
