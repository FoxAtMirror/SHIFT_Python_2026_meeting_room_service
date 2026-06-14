from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    MEETING_ROOM_SERVICE_SECRET_KEY: str

    DATABASE_URL: str

    TEST_DATABASE_URL: str 

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()