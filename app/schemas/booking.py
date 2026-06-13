from datetime import date
from pydantic import BaseModel, ConfigDict



class BookingCreate(BaseModel):

    room_id: int
    slot_id: int
    date: date



class BookingResponse(BaseModel):

    id: int
    room_id: int
    slot_id: int
    date: date


    class Config:

        from_attributes = True