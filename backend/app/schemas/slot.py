from pydantic import (
    BaseModel,
    ConfigDict
)
from datetime import time

class SlotCreate(BaseModel):
    room_id: int
    start_time: time
    end_time: time

class SlotResponse(BaseModel):
    id: int
    room_id: int
    start_time: time
    end_time: time

    model_config = ConfigDict(
        from_attributes=True
    )