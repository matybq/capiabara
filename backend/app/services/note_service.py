from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.user import User
from app.repositories import note_repository
from app.schemas.note import NoteCreate


def create_note(db: Session, note_data: NoteCreate, current_user: User) -> Note:
    """Create a note owned by current_user."""
    return note_repository.create(
        db,
        user_id=current_user.id,
        content=note_data.content,
        title=note_data.title,
    )


def list_notes_by_user(db: Session, current_user: User) -> list[Note]:
    """Return all non-deleted notes for current_user."""
    return note_repository.list_by_user(db, current_user.id)


def get_note(db: Session, note_id: int, current_user: User) -> Note | None:
    """
    Return a note by id scoped to current_user, or None if it does not exist,
    is soft-deleted, or belongs to a different user.
    """
    note = note_repository.get_by_id_and_owner(db, note_id, current_user.id)
    return None if note is None or note.is_deleted else note


def soft_delete_note(db: Session, note_id: int, current_user: User) -> Note | None:
    """Soft-delete a note owned by current_user. Returns None if not found or not owned."""
    return note_repository.soft_delete_by_owner(db, note_id, current_user.id)
