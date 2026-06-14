from fastapi import (
    Request,
    Depends,
    HTTPException
)

from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User

from app.core.security import (
    decode_access_token
)

def get_current_user_ui(
    request: Request,
    db: Session = Depends(get_db)
):

    token = request.cookies.get(
        "access_token"
    )

    if not token:

        return None

    payload = decode_access_token(
        token
    )

    if not payload:

        return None

    user_id = payload.get(
        "sub"
    )

    if not user_id:

        return None

    return (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )

def require_user_ui(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user_ui(
        request,
        db
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    return user