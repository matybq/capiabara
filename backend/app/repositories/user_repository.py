from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def create(db: Session, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def get_by_google_sub(db: Session, google_sub: str) -> User | None:
    stmt = select(User).where(User.google_sub == google_sub)
    return db.execute(stmt).scalar_one_or_none()


def get_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def save(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_active(db: Session) -> list[User]:
    stmt = select(User).where(
        User.is_deleted == False,  # noqa: E712 — SQLAlchemy requires == False, not `is False`
    )
    return list(db.execute(stmt).scalars().all())


def soft_delete(db: Session, user_id: int) -> User | None:
    user = get_by_id(db, user_id)
    if user is None:
        return None
    user.is_deleted = True
    db.commit()
    db.refresh(user)
    return user
