from app.db.models import Slot
from fastapi import HTTPException


class SlotService:

    @staticmethod
    def create_slot(
        db,
        slot
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

    @staticmethod
    def get_room_slots(
        db,
        room_id
    ):

        return (
            db.query(Slot)
            .filter(
                Slot.room_id == room_id
            )
            .all()
        )

    @staticmethod
    def delete_slot(
        db,
        slot_id
    ):

        slot = (
            db.query(Slot)
            .filter(
                Slot.id == slot_id
            )
            .first()
        )

        if not slot:

            raise HTTPException(
                status_code=404,
                detail="Slot not found"
            )

        db.delete(slot)

        db.commit()
    