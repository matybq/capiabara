from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    content: str
    title: str | None = None


class NoteRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    content: str
    title: str | None
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
