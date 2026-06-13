from pydantic import (
    BaseModel,
    ConfigDict
)
class UserCreate(BaseModel):

    login: str
    password: str

class UserResponse(BaseModel):

    id: int
    login: str
    role: str

    model_config = ConfigDict(
        from_attributes=True
    )

class LoginRequest(BaseModel):

    login: str
    password: str

class TokenResponse(BaseModel):

    access_token: str
    token_type: str