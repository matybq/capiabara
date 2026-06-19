from datetime import timedelta
from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.datetime import utcnow
from app.core.exceptions import (
    InactiveUserError,
    InvalidGoogleTokenError,
    UnauthenticatedError,
)
from app.database import get_db

if TYPE_CHECKING:
    from app.models.user import User

_bearer = HTTPBearer(auto_error=False)


def verify_google_token(credential: str) -> dict:
    """
    Verify a Google ID token and return the decoded claims.
    Raises InvalidGoogleTokenError if verification fails.
    """
    try:
        claims = google_id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            audience=settings.google_client_id,
        )
    except Exception as exc:
        raise InvalidGoogleTokenError(str(exc)) from exc

    return {
        "sub": claims["sub"],
        "email": claims.get("email", ""),
        "name": claims.get("name", ""),
        "picture": claims.get("picture", ""),
        "email_verified": claims.get("email_verified", False),
    }


def create_access_token(user: "User") -> str:
    """Issue a 30-day HS256 JWT for the given user."""
    now = utcnow()
    expire = now + timedelta(days=settings.jwt_expiration_days)
    payload = {
        "sub": str(user.id),
        "email": user.email or "",
        "google_sub": user.google_sub or "",
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    """
    Decode and validate an app-issued JWT.
    Raises UnauthenticatedError if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
    except JWTError as exc:
        raise UnauthenticatedError(str(exc)) from exc

    if "sub" not in payload:
        raise UnauthenticatedError("Token missing subject claim.")

    return payload


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> "User":
    """
    FastAPI dependency that resolves the authenticated user from the bearer token.
    Returns the User model instance; raises HTTP 401 for missing/invalid tokens
    and HTTP 403 for inactive or deleted accounts.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(credentials.credentials)
    except UnauthenticatedError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    # Import here to avoid circular imports at module load time
    from app.services import user_service  # noqa: PLC0415

    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    user = user_service.get_user_for_auth(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_service.assert_user_active(user)
    except InactiveUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    return user
