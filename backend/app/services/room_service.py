from app.db.models import (
    Room,
    Slot,
    Booking
)

from datetime import (
    date,
    datetime
)

class RoomService:

    @staticmethod
    def create_room(
        db,
        room
    ):

        db_room = Room(
            name=room.name
        )

        db.add(db_room)

        db.commit()

        db.refresh(db_room)

        return db_room

    @staticmethod
    def get_rooms(db):

        return db.query(Room).all()

    @staticmethod
    def get_room_availability(

        db,
        room_id,
        booking_date
    ):

        slots = (
            db.query(Slot)
            .filter(
                Slot.room_id == room_id
            )
            .order_by(
                Slot.start_time
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

        current_time = (
            datetime.now()
            .time()
        )

        result = []

        for slot in slots:

        
            if (
                booking_date == date.today()
                and slot.end_time <= current_time
            ):
                continue

            result.append(
                {
                    "slot_id": slot.id,
                    "start_time": slot.start_time,
                    "end_time": slot.end_time,
                    "available": (
                        slot.id not in booked_slot_ids
                    )
                }
            )

        return result
    
    @staticmethod
    def get_room_by_id(
        db,
        room_id
    ):

        return (
            db.query(Room)
            .filter(Room.id == room_id)
            .first()
        )