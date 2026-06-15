from sqlalchemy import (
    Column,
    Integer,
    Time,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Slot(Base):

    __tablename__ = "slots"

    id = Column(
        Integer,
        primary_key=True
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
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