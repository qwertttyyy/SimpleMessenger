from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'SimpleMessanger'
    database_url = 'mongodb://localhost:27017'
    database_name: str = 'db'
    secret: str = 'SECRET'
    jwt_lifetime_seconds: int = 3600

    class Config:
        env_file = '.env'


settings = Settings()
