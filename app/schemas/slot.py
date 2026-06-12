from pydantic import BaseModel


class SlotCreate(BaseModel):
    room_id: int
    start_time: str
    end_time: str


class SlotResponse(BaseModel):
    id: int
    room_id: int
    start_time: str
    end_time: str

    class Config:
        from_attributes = True