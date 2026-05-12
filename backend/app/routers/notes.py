from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import UserNotFoundError
from app.database import get_db
from app.schemas.note import NoteCreate, NoteRead
from app.services import note_service

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(note_data: NoteCreate, db: Session = Depends(get_db)):
    try:
        return note_service.create_note(db, note_data)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/", response_model=list[NoteRead])
def get_notes(user_id: int, db: Session = Depends(get_db)):
    """List all non-deleted notes for a user."""
    return note_service.list_notes_by_user(db, user_id)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = note_service.get_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", response_model=NoteRead)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Soft delete: mark note as deleted."""
    note = note_service.soft_delete_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
