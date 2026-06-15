from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User

from app.services.booking_service import BookingService

from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
    BookingAdminResponse,
    UserBookingResponse
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

    return BookingService.create_booking(
        db,
        booking,
        current_user.id
    )

@router.get(
    "/my",
    response_model=list[UserBookingResponse]
)
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return BookingService.get_user_bookings(
    db,
    current_user.id
    )

@router.delete("/{booking_id}")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    BookingService.delete_booking(
    db,
    booking_id,
    current_user
    )

    return {
        "message": "Booking deleted"
    }

@router.get(
    "/",
    response_model=list[BookingAdminResponse],
    dependencies=[Depends(get_admin_user)]
)
def get_all_bookings(
    db: Session = Depends(get_db)
):
    return BookingService.get_all_bookings(db)