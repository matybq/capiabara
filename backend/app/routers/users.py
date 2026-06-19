from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserCurrentRead, UserRead
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserCurrentRead)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the authenticated user's own profile."""
    return UserCurrentRead.model_validate(current_user)


@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a user manually. Only available when DEBUG=true.
    In production (DEBUG=false) this endpoint returns 403.
    """
    if not settings.debug:
        raise HTTPException(status_code=403, detail="Manual user creation is disabled.")
    return user_service.create_user(db, user_data)
