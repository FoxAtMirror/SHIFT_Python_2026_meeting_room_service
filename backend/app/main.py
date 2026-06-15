from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.db.database import engine, Base
from app.db.models import (
    User,
    Room,
    Slot,
    Booking
)
from app.api import (
    slots,
    auth,
    bookings,
    rooms
)

from fastapi.middleware.cors import CORSMiddleware

def create_admin():

    db = Session(bind=engine)

    admin = (
        db.query(User)
        .filter(
            User.login == "admin"
        )
        .first()
    )

    if not admin:

        admin = User(
            login="admin",
            password_hash=hash_password(
                "admin"
            ),
            role="admin"
        )

        db.add(admin)

        db.commit()

    db.close()

@asynccontextmanager
async def lifespan(app):

    Base.metadata.create_all(bind=engine)
    create_admin()
    yield

app = FastAPI(
    title="Meeting Room Booking Service",   
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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