from app.db.models import Slot
from fastapi import HTTPException


class SlotService:

    @staticmethod
    def create_slot(
        db,
        slot
    ):

        if slot.start_time >= slot.end_time:

            raise HTTPException(
                status_code=400,
                detail="Start time must be earlier than end time"
            )
        

        existing_slots = (
            db.query(Slot)
            .filter(
                Slot.room_id == slot.room_id
            )
            .all()
        )

        for existing_slot in existing_slots:

            if (
                slot.start_time < existing_slot.end_time
                and slot.end_time > existing_slot.start_time
            ):

                raise HTTPException(
                    status_code=400,
                    detail="Slot overlaps with existing slot"
                )

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
            .order_by(
                Slot.start_time
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
    