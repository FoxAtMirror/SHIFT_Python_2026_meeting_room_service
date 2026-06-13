from fastapi import FastAPI

from app.db.test_database import (
    engine,
    TestingSessionLocal
)
from app.db.models import Base

from app.api import auth
from app.api import rooms
from app.api import slots
from app.api import bookings

Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Meeting Room Booking Service"
)

app.include_router(
    auth.router
)
app.include_router(
    rooms.router
)
app.include_router(
    slots.router
)
app.include_router(
    bookings.router
)

@app.get("/")
def root():
    return {
        "message": "Service is running"
    }