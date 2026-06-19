from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.auth import router as auth_router
from app.routers.notes import router as notes_router
from app.routers.users import router as users_router

# Fail fast if auth secrets are missing — Alembic imports settings too but
# only needs database_url, so validation lives here rather than in Settings.
settings.validate_auth_settings()

app = FastAPI(title="CapIAbara API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.include_router(auth_router)
app.include_router(notes_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {"status": "ok", "service": "capiabara"}
