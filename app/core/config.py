from pathlib import Path

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'SimpleMessanger'
    database_url = 'mongodb://localhost:27017'
    database_name: str = 'db'
    secret: str = 'SECRET'
    base_url: str = 'http://localhost'
    port: int = 8000
    jwt_lifetime_seconds: int = 3600
    media_folder = Path(__file__).resolve().parent.parent / "media"

    class Config:
        env_file = '.env'


settings = Settings()
