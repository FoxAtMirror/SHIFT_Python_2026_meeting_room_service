from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services.room_service import RoomService

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

    return RoomService.create_room(
        db,
        room
    )

@router.get(
    "",
    response_model=list[RoomResponse]
)
def get_rooms(
    db: Session = Depends(get_db)
):

    return RoomService.get_rooms(
        db
    )

@router.get("/{room_id}/availability")
def room_availability(
    room_id: int,
    booking_date: date,
    db: Session = Depends(get_db)
):

    return RoomService.get_room_availability(
    db,
    room_id,
    booking_date
    )   