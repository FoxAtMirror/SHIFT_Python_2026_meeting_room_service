from app.db.models import Slot


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