from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import (
    Booking,
    User
)

from app.schemas.booking import (
    BookingCreate,
    BookingResponse
)

from app.core.dependencies import (
    get_current_user,
    get_admin_user
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post(
    "",
    response_model=BookingResponse
)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    existing_booking = (
        db.query(Booking)
        .filter(
            Booking.room_id == booking.room_id,
            Booking.slot_id == booking.slot_id,
            Booking.date == booking.date
        )
        .first()
    )

    if existing_booking:

        raise HTTPException(
            status_code=400,
            detail="Slot already booked"
        )

    db_booking = Booking(
        room_id=booking.room_id,
        slot_id=booking.slot_id,
        date=booking.date,
        user_id=current_user.id
    )

    db.add(db_booking)

    db.commit()

    db.refresh(db_booking)

    return db_booking

@router.get(
    "/my",
    response_model=list[BookingResponse]
)
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return (
        db.query(Booking)
        .filter(
            Booking.user_id == current_user.id
        )
        .all()
    )

@router.delete("/{booking_id}")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if (
        booking.user_id != current_user.id
        and current_user.role != "admin"
    ):

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    db.delete(booking)

    db.commit()

    return {
        "message": "Booking deleted"
    }

@router.get("/")
def get_all_bookings(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):

    return db.query(Booking).all()