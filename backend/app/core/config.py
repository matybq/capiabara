from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class Config(BaseSettings):
    app_name: str = "CapIAbara API"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = "test.db"

    @property
    def db_url(self):
        return f"sqlite:///./{self.db_name}"


config = Config()
