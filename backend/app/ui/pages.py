from fastapi import (
    APIRouter,
    Request,
    Form,
    Depends,
    HTTPException
)

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services.auth_service import authenticate_user
from app.services.room_service import RoomService
from app.services.booking_service import BookingService

from app.core.security import create_access_token

from datetime import date

from app.ui.dependencies_ui import (
    get_current_user_ui,
    get_admin_user_ui
)

from app.schemas.booking import BookingCreate
from app.schemas.room import RoomCreate
from app.services.booking_service import BookingService

from app.services.slot_service import SlotService
from app.schemas.slot import SlotCreate

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/")
def home(
    request: Request,
    current_user = Depends(
        get_current_user_ui
    )
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "current_user": current_user
        }
    )

@router.get("/login")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

@router.post("/login")
def login(
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        username,
        password
    )

    if not user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role
        }
    )

    response = RedirectResponse(
        "/rooms",
        status_code=303
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )

    return response

@router.get("/rooms")
def rooms_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user_ui
    )
):

    rooms = RoomService.get_rooms(db)

    return templates.TemplateResponse(
        request=request,
        name="rooms_list.html",
        context={
            "rooms": rooms,
            "current_user": current_user
        }
    )

@router.get("/rooms/{room_id}")
def room_page(
    room_id: int,
    request: Request,
    booking_date: date | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(
    get_current_user_ui
)
):

    room = RoomService.get_room_by_id(
    db,
    room_id
)

    if room is None:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )
    
    if booking_date is None:
        booking_date = date.today()


    availability = (
        RoomService.get_room_availability(
            db,
            room_id,
            booking_date
        )
    )

    return templates.TemplateResponse(
    request=request,
    name="room_details.html",
    context={
        "room": room,
        "availability": availability,
        "booking_date": booking_date,
        "current_user": current_user
    }
)

@router.get("/my-bookings")
def my_bookings_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user_ui
    )
):

    if not current_user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    bookings = (
        BookingService.get_user_bookings(
            db,
            current_user.id
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="my_bookings.html",
        context={
            "current_user": current_user,
            "bookings": bookings
        }
    )

@router.post("/my-bookings/{booking_id}/delete")
def delete_booking_ui(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user_ui
    )
):

    if not current_user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    BookingService.delete_booking(
        db,
        booking_id,
        current_user
    )

    return RedirectResponse(
        "/my-bookings",
        status_code=303
    )

@router.post("/rooms/{room_id}/book")
def create_booking_ui(
    room_id: int,
    slot_id: int = Form(),
    booking_date: date = Form(),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_ui)
):

    if not current_user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    booking = BookingCreate(
        room_id=room_id,
        slot_id=slot_id,
        date=booking_date
    )

    BookingService.create_booking(
        db,
        booking,
        current_user.id
    )

    return RedirectResponse(
        f"/rooms/{room_id}?booking_date={booking_date}",
        status_code=303
    )

@router.get("/admin")
def admin_page(
    request: Request,
    current_user = Depends(
        get_admin_user_ui
    )
):

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={
            "current_user": current_user
        }
    )

@router.get("/admin/rooms")
def admin_rooms_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_admin_user_ui
    )
):

    rooms = RoomService.get_rooms(db)

    return templates.TemplateResponse(
        request=request,
        name="admin_rooms.html",
        context={
            "current_user": current_user,
            "rooms": rooms
        }
    )

@router.post("/admin/rooms")
def create_room_ui(
    room_name: str = Form(),
    db: Session = Depends(get_db),
    current_user = Depends(
        get_admin_user_ui
    )
):

    room = RoomCreate(
        name=room_name
    )

    RoomService.create_room(
        db,
        room
    )

    return RedirectResponse(
        "/admin/rooms",
        status_code=303
    )

@router.get("/admin/slots")
def admin_slots_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_admin_user_ui
    )
):

    rooms = RoomService.get_rooms(db)

    slots = []

    for room in rooms:

        room_slots = (
            SlotService.get_room_slots(
                db,
                room.id
            )
        )

        slots.extend(room_slots)

    return templates.TemplateResponse(
        request=request,
        name="admin_slots.html",
        context={
            "current_user": current_user,
            "rooms": rooms,
            "slots": slots
        }
    )

@router.post("/admin/slots")
def create_slot_ui(
    room_id: int = Form(),
    start_time: str = Form(),
    end_time: str = Form(),
    db: Session = Depends(get_db),
    current_user = Depends(
        get_admin_user_ui
    )
):

    slot = SlotCreate(
        room_id=room_id,
        start_time=start_time,
        end_time=end_time
    )

    SlotService.create_slot(
        db,
        slot
    )

    return RedirectResponse(
        "/admin/slots",
        status_code=303
    )

@router.get("/logout")
def logout():

    response = RedirectResponse(
        "/",
        status_code=303
    )

    response.delete_cookie(
        "access_token"
    )

    return response

@router.post("/admin/slots/{slot_id}/delete")
def delete_slot_ui(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_admin_user_ui
    )
):

    SlotService.delete_slot(
        db,
        slot_id
    )

    return RedirectResponse(
        "/admin/slots",
        status_code=303
    )