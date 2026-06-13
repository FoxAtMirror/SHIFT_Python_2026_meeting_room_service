from pydantic import (
    BaseModel,
    ConfigDict
)
class SlotCreate(BaseModel):
    room_id: int
    start_time: str
    end_time: str

class SlotResponse(BaseModel):
    id: int
    room_id: int
    start_time: str
    end_time: str

    model_config = ConfigDict(
        from_attributes=True
    )