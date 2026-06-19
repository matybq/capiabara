from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.note import Note


def create(db: Session, user_id: int, content: str, title: str | None) -> Note:
    note = Note(user_id=user_id, content=content, title=title)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_by_id(db: Session, note_id: int) -> Note | None:
    stmt = select(Note).where(Note.id == note_id)
    return db.execute(stmt).scalar_one_or_none()


def get_by_id_and_owner(db: Session, note_id: int, user_id: int) -> Note | None:
    """Return a note only if it belongs to the given user."""
    stmt = select(Note).where(Note.id == note_id, Note.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def list_by_user(db: Session, user_id: int) -> list[Note]:
    stmt = select(Note).where(
        Note.user_id == user_id,
        Note.is_deleted == False,  # noqa: E712 — SQLAlchemy requires == False, not `is False`
    )
    return list(db.execute(stmt).scalars().all())


def soft_delete(db: Session, note_id: int) -> Note | None:
    note = get_by_id(db, note_id)
    if note is None:
        return None
    note.is_deleted = True
    db.commit()
    db.refresh(note)
    return note


def soft_delete_by_owner(db: Session, note_id: int, user_id: int) -> Note | None:
    """Soft-delete a note only if it belongs to the given user."""
    note = get_by_id_and_owner(db, note_id, user_id)
    if note is None:
        return None
    note.is_deleted = True
    db.commit()
    db.refresh(note)
    return note
