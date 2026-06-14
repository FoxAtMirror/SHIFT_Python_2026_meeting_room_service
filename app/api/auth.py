from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User

from app.schemas.user import (
    UserCreate,
    TokenResponse
)

from app.services.auth_service import (
    create_user,
    authenticate_user
)

from app.core.security import create_access_token

from app.core.dependencies import (
    get_current_user,
    get_admin_user
)
 

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)



@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = create_user(
        db,
        user.login,
        user.password
    )


    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )


    return new_user


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid login or password"
        )

    token = create_access_token(
        {
            "sub": str(db_user.id),
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "login": current_user.login,
        "role": current_user.role
    }


@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):

    return db.query(User).all()