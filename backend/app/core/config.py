from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "CapIAbara API"
    debug: bool = False
    database_url: str = "sqlite:///./capiabara.db"

    # Google OAuth
    google_client_id: str = ""

    # App-issued JWT
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_issuer: str = "capiabara"
    jwt_audience: str = "capiabara"
    jwt_expiration_days: int = 30

    # CORS — comma-separated list of allowed origins; never use wildcard in production
    cors_origins: str = "http://localhost:5173"

    def validate_auth_settings(self) -> None:
        """Raise ValueError if auth secrets required at runtime are missing.

        Call this from FastAPI app startup and auth paths — not from Alembic,
        which only needs database_url.
        """
        if not self.jwt_secret:
            raise ValueError(
                "JWT_SECRET must be set to a non-empty value. "
                "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        if not self.google_client_id:
            raise ValueError(
                "GOOGLE_CLIENT_ID must be set to a non-empty value. "
                "Obtain it from the Google Cloud Console."
            )

    def get_cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
