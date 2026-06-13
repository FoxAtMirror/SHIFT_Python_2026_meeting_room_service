from sqlalchemy import (
    Column,
    Integer,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Booking(Base):

    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True
    )

    date = Column(
        Date,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    room_id = Column(
        Integer,
        ForeignKey("rooms.id")
    )

    slot_id = Column(
        Integer,
        ForeignKey("slots.id")
    )

    user = relationship(
        "User",
        back_populates="bookings"
    )

    room = relationship(
        "Room",
        back_populates="bookings"
    )

    slot = relationship(
        "Slot"
    )