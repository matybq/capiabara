from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import InactiveUserError, InvalidGoogleTokenError
from app.core.security import create_access_token, get_current_user, verify_google_token
from app.database import get_db
from app.models.user import User
from app.schemas.auth import AuthSessionResponse, GoogleTokenRequest
from app.schemas.user import UserCurrentRead
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["auth"])


def _build_session_response(user: User) -> AuthSessionResponse:
    from app.core.config import settings  # noqa: PLC0415

    token = create_access_token(user)
    return AuthSessionResponse(
        token=token,
        expires_in=settings.jwt_expiration_days * 86400,
        user=UserCurrentRead.model_validate(user),
    )


@router.post("/google", response_model=AuthSessionResponse, status_code=200)
def google_sign_in(body: GoogleTokenRequest, db: Session = Depends(get_db)):
    """Exchange a Google ID token for an app JWT."""
    try:
        claims = verify_google_token(body.credential)
    except InvalidGoogleTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {exc}",
        ) from exc

    try:
        user = user_service.get_or_create_from_google(db, claims)
    except InactiveUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    return _build_session_response(user)


@router.get("/me", response_model=UserCurrentRead)
def get_session(current_user: User = Depends(get_current_user)):
    """Return the authenticated user's profile."""
    return UserCurrentRead.model_validate(current_user)
