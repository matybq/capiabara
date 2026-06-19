from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str


class UserRead(BaseModel):
    """Public user profile — does not expose google_sub."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    is_deleted: bool


class UserCurrentRead(BaseModel):
    """Internal/session shape returned to the authenticated user; includes google_sub."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str | None
    google_sub: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
