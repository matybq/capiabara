from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)


@router.get("/", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    """List all non-deleted users."""
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=UserRead)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Soft delete: mark user as deleted."""
    user = user_service.soft_delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
