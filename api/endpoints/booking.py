from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models import Booking, UserModel, CarModel
from .depends.db import get_session
from .depends.auth import current_user
from schemas import BookingCreate, BookingRead, BookingUpdate
from models import UserRoles

router = APIRouter(
    prefix="/booking",
    tags=["booking"],
)

# --- Пользовательские точки ---

@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_in: BookingCreate,
    session: AsyncSession = Depends(get_session),
    user: UserModel = Depends(current_user),
):
    car = await session.get(CarModel, booking_in.car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    if user.balance < car.price_per_day:
        raise HTTPException(status_code=400, detail="Not enough balance")
        
    booking = Booking(
        user_id=user.id,
        car_id=booking_in.car_id,
        date_start=booking_in.date_start,
        date_end=booking_in.date_end,
    )
    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    return booking

@router.get("/", response_model=list[BookingRead])
async def get_user_bookings(
    session: AsyncSession = Depends(get_session),
    user: UserModel = Depends(current_user),
):
    stmt = (
        select(Booking)
        .where(Booking.user_id == user.id)
        .options(
            selectinload(Booking.car).selectinload(CarModel.car_brand),
            selectinload(Booking.car).selectinload(CarModel.transmission),
            selectinload(Booking.car).selectinload(CarModel.engine_type),
            selectinload(Booking.car).selectinload(CarModel.rental_class),
            selectinload(Booking.car).selectinload(CarModel.body),
            selectinload(Booking.car).selectinload(CarModel.drive),
            selectinload(Booking.car).selectinload(CarModel.images),
        )
    )
    result = await session.execute(stmt)
    return result.scalars().all()

@router.get("/{booking_id}", response_model=BookingRead)
async def get_user_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_session),
    user: UserModel = Depends(current_user),
):
    stmt = (
        select(Booking)
        .where(Booking.id == booking_id)
        .options(
            selectinload(Booking.car).selectinload(CarModel.car_brand),
            selectinload(Booking.car).selectinload(CarModel.transmission),
            selectinload(Booking.car).selectinload(CarModel.engine_type),
            selectinload(Booking.car).selectinload(CarModel.rental_class),
            selectinload(Booking.car).selectinload(CarModel.body),
            selectinload(Booking.car).selectinload(CarModel.drive),
            selectinload(Booking.car).selectinload(CarModel.images),
        )
    )
    result = await session.execute(stmt)
    booking = result.scalars().first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return booking

# --- Админские точки ---

@router.get("/admin/all", response_model=list[BookingRead])
async def get_all_bookings(
    session: AsyncSession = Depends(get_session),
    user: UserModel = Depends(current_user),
):
    if user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    stmt = (
        select(Booking)
        .options(
            selectinload(Booking.car).selectinload(CarModel.car_brand),
            selectinload(Booking.car).selectinload(CarModel.transmission),
            selectinload(Booking.car).selectinload(CarModel.engine_type),
            selectinload(Booking.car).selectinload(CarModel.rental_class),
            selectinload(Booking.car).selectinload(CarModel.body),
            selectinload(Booking.car).selectinload(CarModel.drive),
            selectinload(Booking.car).selectinload(CarModel.images),
        )
    )
    result = await session.execute(stmt)
    return result.scalars().all()

@router.get("/admin/{booking_id}", response_model=BookingRead)
async def get_any_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_session),
    user: UserModel = Depends(current_user),
):
    if user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    stmt = (
        select(Booking)
        .where(Booking.id == booking_id)
        .options(
            selectinload(Booking.car).selectinload(CarModel.car_brand),
            selectinload(Booking.car).selectinload(CarModel.transmission),
            selectinload(Booking.car).selectinload(CarModel.engine_type),
            selectinload(Booking.car).selectinload(CarModel.rental_class),
            selectinload(Booking.car).selectinload(CarModel.body),
            selectinload(Booking.car).selectinload(CarModel.drive),
            selectinload(Booking.car).selectinload(CarModel.images),
        )
    )
    result = await session.execute(stmt)
    booking = result.scalars().first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.patch("/admin/{booking_id}", response_model=BookingRead)
async def update_any_booking(
    booking_id: int,
    booking_in: BookingUpdate,
    session: AsyncSession = Depends(get_session),
    user: UserModel = Depends(current_user),
):
    if user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    booking = await session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    for field, value in booking_in.dict(exclude_unset=True).items():
        setattr(booking, field, value)
    await session.commit()
    await session.refresh(booking)
    return booking

@router.delete("/admin/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_any_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_session),
    user: UserModel = Depends(current_user),
):
    if user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    booking = await session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    await session.delete(booking)
    await session.commit()