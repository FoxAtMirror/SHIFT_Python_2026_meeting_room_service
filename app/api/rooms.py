from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import (
    Slot,
    Booking,
    Room
)

from app.schemas.room import (
    RoomCreate,
    RoomResponse
)

from datetime import date



router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)

@router.post(
    "",
    response_model=RoomResponse
)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db)
):

    db_room = Room(
        name=room.name
    )

    db.add(db_room)

    db.commit()

    db.refresh(db_room)

    return db_room

@router.get(
    "",
    response_model=list[RoomResponse]
)
def get_rooms(
    db: Session = Depends(get_db)
):

    return db.query(Room).all()

@router.get("/{room_id}/availability")
def room_availability(
    room_id: int,
    booking_date: date,
    db: Session = Depends(get_db)
):

    slots = (
        db.query(Slot)
        .filter(
            Slot.room_id == room_id
        )
        .all()
    )

    bookings = (
        db.query(Booking)
        .filter(
            Booking.room_id == room_id,
            Booking.date == booking_date
        )
        .all()
    )

    booked_slot_ids = {
        booking.slot_id
        for booking in bookings
    }

    return [
        {
            "slot_id": slot.id,
            "start_time": slot.start_time,
            "end_time": slot.end_time,
            "available": slot.id not in booked_slot_ids
        }
        for slot in slots
    ]