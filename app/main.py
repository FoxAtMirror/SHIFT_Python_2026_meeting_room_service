from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine, Base
from app.db.models import (
    User,
    Room,
    Slot,
    Booking
)
from app.api import (
    auth,
    rooms,
    slots,
    bookings
)

@asynccontextmanager
async def lifespan(app):

    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="Meeting Room Booking Service",
    lifespan=lifespan
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