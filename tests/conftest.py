from fastapi.testclient import TestClient

from app.main import app

from app.db.database import get_db
from app.db.test_database import (
    engine,
    TestingSessionLocal
)
from app.db.database import Base
from app.db.models import (
    Booking,
    Slot,
    Room,
    User
)

import pytest


Base.metadata.create_all(bind=engine)


def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = (
    override_get_db
)


@pytest.fixture
def client():

    yield TestClient(app)


@pytest.fixture(autouse=True)
def clear_database():

    db = TestingSessionLocal()

    db.query(Booking).delete()
    db.query(Slot).delete()
    db.query(Room).delete()
    db.query(User).delete()

    db.commit()
    db.close()

    yield