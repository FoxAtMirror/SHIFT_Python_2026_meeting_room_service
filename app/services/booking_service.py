from fastapi import HTTPException

from app.db.models import Booking


class BookingService:

    @staticmethod
    def create_booking(
        db,
        booking,
        user_id
    ):

        existing_booking = (
            db.query(Booking)
            .filter(
                Booking.room_id == booking.room_id,
                Booking.slot_id == booking.slot_id,
                Booking.date == booking.date
            )
            .first()
        )

        if existing_booking:

            raise HTTPException(
                status_code=400,
                detail="Slot already booked"
            )

        db_booking = Booking(
            room_id=booking.room_id,
            slot_id=booking.slot_id,
            date=booking.date,
            user_id=user_id
        )

        db.add(db_booking)

        db.commit()

        db.refresh(db_booking)

        return db_booking

    @staticmethod
    def get_user_bookings(
        db,
        user_id
    ):

        return (
            db.query(Booking)
            .filter(
                Booking.user_id == user_id
            )
            .all()
        )

    @staticmethod
    def delete_booking(
        db,
        booking_id,
        current_user
    ):

        booking = (
            db.query(Booking)
            .filter(
                Booking.id == booking_id
            )
            .first()
        )

        if not booking:

            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        if (
            booking.user_id != current_user.id
            and current_user.role != "admin"
        ):

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        db.delete(booking)

        db.commit()

    @staticmethod
    def get_all_bookings(db):

        return db.query(Booking).all()