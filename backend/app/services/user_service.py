from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repository
from app.schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user."""
    return user_repository.create(db, user_data)


def list_users(db: Session) -> list[User]:
    """Return all non-deleted users."""
    return user_repository.list_active(db)


def get_user(db: Session, user_id: int) -> User | None:
    """
    Return a user by id, or None if it does not exist or is soft-deleted.
    """
    user = user_repository.get_by_id(db, user_id)
    if user is None or user.is_deleted:
        return None
    return user


def soft_delete_user(db: Session, user_id: int) -> User | None:
    """
    Soft-delete a user. Returns the updated user, or None if not found.
    Notes are not cascaded — ownership records remain intact.
    """
    return user_repository.soft_delete(db, user_id)
