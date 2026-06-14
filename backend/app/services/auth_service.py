from sqlalchemy.orm import Session

from app.db.models import User
from app.core.security import (
    hash_password,
    verify_password
)

def create_user(
    db: Session,
    login: str,
    password: str
):

    existing_user = (
        db.query(User)
        .filter(User.login == login)
        .first()
    )

    if existing_user:
        return None


    user = User(
        login=login,
        password_hash=hash_password(password),
        role="employee"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(
    db: Session,
    login: str,
    password: str
):

    user = (
        db.query(User)
        .filter(User.login == login)
        .first()
    )


    if not user:
        return None


    if not verify_password(
        password,
        user.password_hash
    ):
        return None


    return user