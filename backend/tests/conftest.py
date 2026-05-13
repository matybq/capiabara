import os

# Prevent app.database from connecting to any local .env DATABASE_URL on import.
# This must run before any app module is imported.
os.environ["DATABASE_URL"] = "sqlite://"
# Enable debug mode so POST /users/ (manual creation) is available in tests.
os.environ.setdefault("DEBUG", "true")
# Provide required secrets so Settings validation passes without a real .env.
os.environ.setdefault("JWT_SECRET", "test-jwt-secret-not-for-production")
os.environ.setdefault("GOOGLE_CLIENT_ID", "test-google-client-id.apps.googleusercontent.com")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models.user  # noqa: F401 — ensure User table is registered in metadata
import app.models.note  # noqa: F401 — ensure Note table is registered in metadata
from app.core.security import get_current_user
from app.database import Base, get_db
from app.main import app as fastapi_app
from app.models.user import User

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def _make_test_user(db):
    """Return (or create) a stable test user for auth overrides."""
    user = db.query(User).filter_by(name="__test_auth_user__").first()
    if user is None:
        user = User(name="__test_auth_user__", email="test@example.com", is_active=True)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    def override_get_db():
        try:
            yield db
        finally:
            pass  # db closed after fixture teardown

    def override_get_current_user():
        return _make_test_user(db)

    fastapi_app.dependency_overrides[get_db] = override_get_db
    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(fastapi_app) as c:
        yield c

    fastapi_app.dependency_overrides.clear()
    db.close()
    Base.metadata.drop_all(bind=test_engine)
