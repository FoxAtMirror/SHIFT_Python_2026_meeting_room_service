from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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
from app.ui import pages

from app.ui.middleware import AuthMiddleware


@asynccontextmanager
async def lifespan(app):

    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Meeting Room Booking Service",
    lifespan=lifespan
)

app.add_middleware(
    AuthMiddleware
)
app.include_router(
    auth.router,
    prefix="/api"
)
app.include_router(
    rooms.router,
    prefix="/api"
)
app.include_router(
    slots.router,
    prefix="/api"
)
app.include_router(
    bookings.router,
    prefix="/api"
)
app.include_router(
    pages.router
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)
