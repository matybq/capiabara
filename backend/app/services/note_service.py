from sqlalchemy.orm import Session

from app.models.note import Note
from app.repositories import note_repository
from app.schemas.note import NoteCreate


def create_note(db: Session, note_data: NoteCreate) -> Note:
    """Create a new note."""
    return note_repository.create(db, note_data)


def list_notes_by_user(db: Session, user_id: str) -> list[Note]:
    """Return all non-deleted notes for a user."""
    return note_repository.list_by_user(db, user_id)


def get_note(db: Session, note_id: int) -> Note | None:
    """
    Return a note by id, or None if it does not exist or is soft-deleted.
    """
    note = note_repository.get_by_id(db, note_id)
    return None if note is None or note.is_deleted else note


def soft_delete_note(db: Session, note_id: int) -> Note | None:
    """
    Soft-delete a note. Returns the updated note, or None if not found.
    """
    return note_repository.soft_delete(db, note_id)
