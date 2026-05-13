from sqlalchemy.orm import Session

from app.core.exceptions import InactiveUserError
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
    """Return a user by id, or None if it does not exist or is soft-deleted."""
    user = user_repository.get_by_id(db, user_id)
    return None if user is None or user.is_deleted else user


def get_user_for_auth(db: Session, user_id: int) -> User | None:
    """Return a user by id for auth resolution; does not filter by active/deleted state."""
    return user_repository.get_by_id(db, user_id)


def assert_user_active(user: User) -> None:
    """Raise InactiveUserError if the user is soft-deleted or inactive."""
    if user.is_deleted or not user.is_active:
        raise InactiveUserError("This account is inactive or has been deleted.")


def soft_delete_user(db: Session, user_id: int) -> User | None:
    """
    Soft-delete a user. Returns the updated user, or None if not found.
    Notes are not cascaded — ownership records remain intact.
    """
    return user_repository.soft_delete(db, user_id)


def get_or_create_from_google(db: Session, claims: dict) -> User:
    """
    Resolve a Google login to a local user account.

    Resolution order:
    1. Match by google_sub (primary identity).
    2. Match by email (legacy fallback for pre-existing local rows).
    3. Create a new user if neither exists.

    Raises InactiveUserError if the matched account is deleted or inactive.
    """
    google_sub: str = claims["sub"]
    email: str = claims.get("email", "")
    email_verified: bool = bool(claims.get("email_verified", False))
    name: str = claims.get("name", "") or email

    user = user_repository.get_by_google_sub(db, google_sub)

    if user is None and email and email_verified:
        user = user_repository.get_by_email(db, email)
        if user is not None:
            # Link the existing row to this Google identity (only when email is verified)
            user.google_sub = google_sub

    if user is None:
        user = User(name=name, email=email or None, google_sub=google_sub)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    assert_user_active(user)

    # Update identity fields if they changed
    if user.email is None and email:
        user.email = email
    if user.name != name and name:
        user.name = name

    return user_repository.save(db, user)
