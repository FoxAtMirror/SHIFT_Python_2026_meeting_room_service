from sqlalchemy import (
    Column,
    Integer,
    String
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Room(Base):

    __tablename__ = "rooms"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    slots = relationship(
        "Slot",
        back_populates="room"
    )

    bookings = relationship(
        "Booking",
        back_populates="room"
    )