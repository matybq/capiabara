from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.note import Note
from app.schemas.note import NoteCreate


def create(db: Session, note_data: NoteCreate) -> Note:
    """
    Crea una nueva nota. Equivalente Rails: Note.create!(...)
    """
    note = Note(**note_data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_by_id(db: Session, note_id: int) -> Note | None:
    """
    Devuelve una nota por id (incluyendo las soft-deleted).
    Equivalente Rails: Note.find_by(id: note_id)
    """
    stmt = select(Note).where(Note.id == note_id)
    return db.execute(stmt).scalar_one_or_none()


def list_by_user(db: Session, user_id: str) -> list[Note]:
    """
    Devuelve todas las notas no eliminadas de un usuario.
    Equivalente Rails: Note.where(user_id: user_id, is_deleted: false)
    """
    stmt = select(Note).where(
        Note.user_id == user_id,
        Note.is_deleted == False,  # noqa: E712 — SQLAlchemy requiere == False
    )
    return list(db.execute(stmt).scalars().all())


def soft_delete(db: Session, note_id: int) -> Note | None:
    """
    Marca una nota como eliminada. No borra el registro.
    Equivalente Rails: note.update!(is_deleted: true)
    """
    note = get_by_id(db, note_id)
    if note is None:
        return None
    note.is_deleted = True
    db.commit()
    db.refresh(note)
    return note
