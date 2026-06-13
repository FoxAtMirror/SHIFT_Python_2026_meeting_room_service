from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SECRET_KEY: str

    DATABASE_URL: str

    TEST_DATABASE_URL: str = (
        "postgresql://postgres:0000@localhost:5432/meeting_room_test"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()