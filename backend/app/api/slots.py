from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services.slot_service import SlotService

from app.schemas.slot import (
    SlotCreate,
    SlotResponse
)

from app.core.dependencies import get_admin_user
from app.db.models import User


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
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):

    return SlotService.create_slot(
    db,
    slot
)

@router.get(
    "/room/{room_id}",
    response_model=list[SlotResponse]
)
def get_room_slots(
    room_id: int,
    db: Session = Depends(get_db)
):

    return SlotService.get_room_slots(
        db,
        room_id
    )