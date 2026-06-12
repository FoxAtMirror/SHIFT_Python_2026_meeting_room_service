from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Slot

from app.schemas.slot import (
    SlotCreate,
    SlotResponse
)


router = APIRouter(
    prefix="/slots",
    tags=["Slots"]
)

@router.post(
    "",
    response_model=SlotResponse
)
def create_slot(
    slot: SlotCreate,
    db: Session = Depends(get_db)
):

    db_slot = Slot(
        room_id=slot.room_id,
        start_time=slot.start_time,
        end_time=slot.end_time
    )

    db.add(db_slot)

    db.commit()

    db.refresh(db_slot)

    return db_slot

@router.get(
    "/room/{room_id}",
    response_model=list[SlotResponse]
)
def get_room_slots(
    room_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(Slot)
        .filter(Slot.room_id == room_id)
        .all()
    )