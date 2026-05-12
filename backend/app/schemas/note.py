from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    """
    Schema para el body del POST /notes.
    Equivalente Rails: strong params en el controller.
    """

    user_id: str
    content: str
    title: str | None = None


class NoteRead(BaseModel):
    """
    Schema para todas las respuestas de la API.
    Equivalente Rails: serializer (jbuilder / active_model_serializers).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    content: str
    title: str | None
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
