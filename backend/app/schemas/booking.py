from datetime import date

from pydantic import (
    BaseModel,
    ConfigDict
)

class BookingCreate(BaseModel):

    room_id: int
    slot_id: int
    date: date

class BookingResponse(BaseModel):

    id: int
    room_id: int
    slot_id: int
    date: date

    model_config = ConfigDict(
        from_attributes=True
    )

class BookingAdminResponse(BaseModel):
    
    id: int
    user_login: str
    room_name: str
    slot_time: str
    date: date

class UserBookingResponse(BaseModel):

    id: int
    room_name: str
    slot_time: str
    date: date