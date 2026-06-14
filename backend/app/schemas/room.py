from pydantic import (
    BaseModel,
    ConfigDict
)
class RoomCreate(BaseModel):
    name: str

class RoomResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )