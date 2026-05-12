from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.note import Note
from app.schemas.note import NoteCreate


def create(db: Session, note_data: NoteCreate) -> Note:
    note = Note(**note_data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_by_id(db: Session, note_id: int) -> Note | None:
    stmt = select(Note).where(Note.id == note_id)
    return db.execute(stmt).scalar_one_or_none()


def list_by_user(db: Session, user_id: str) -> list[Note]:
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
