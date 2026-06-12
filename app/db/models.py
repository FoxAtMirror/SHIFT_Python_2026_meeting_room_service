from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    login = Column(
        String,
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="employee"
    )


    bookings = relationship(
        "Booking",
        back_populates="user"
    )



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



class Slot(Base):

    __tablename__ = "slots"


    id = Column(
        Integer,
        primary_key=True
    )


    start_time = Column(
        String,
        nullable=False
    )


    end_time = Column(
        String,
        nullable=False
    )


    room_id = Column(
        Integer,
        ForeignKey("rooms.id")
    )


    room = relationship(
        "Room",
        back_populates="slots"
    )



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