from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base


TEST_DATABASE_URL = (
    "postgresql://postgres:0000@localhost:5432/meeting_room_test"
)


engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)