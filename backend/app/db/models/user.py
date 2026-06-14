from sqlalchemy import (
    Column,
    Integer,
    String
)

from sqlalchemy.orm import relationship

from app.db.database import Base


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