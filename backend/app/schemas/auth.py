from pydantic import BaseModel

from app.schemas.user import UserCurrentRead


class GoogleTokenRequest(BaseModel):
    credential: str


class AuthSessionResponse(BaseModel):
    token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserCurrentRead
