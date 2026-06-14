from app.db.models import (
    Room,
    Slot,
    Booking
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
                "available": (
                    slot.id not in booked_slot_ids
                )
            }
            for slot in slots
        ]
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