from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import note_repository
from app.schemas.note import NoteCreate, NoteRead

""" /notes is the prefix for this router , all routes scopes to it"""
router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model = NoteRead, status_code=201)
def create_note(note_data: NoteCreate, db: Session = Depends(get_db)):
    return note_repository.create(db, note_data)


@router.get("/", response_model = list[NoteRead])
def get_notes(user_id: str, db: Session = Depends(get_db)):
    """List all the NO deleted notes of a user."""
    return note_repository.list_by_user(db, user_id)


@router.get("/{note_id}", response_model = NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = note_repository.get_by_id(db, note_id)
    if note is None or note.is_deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", response_model = NoteRead)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Soft delete: mark note as deleted."""
    note = note_repository.soft_delete(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
