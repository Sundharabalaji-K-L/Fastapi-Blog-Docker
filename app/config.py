from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    MONGO_DB_USER: str
    MONGO_DB_PASSWORD: str
    MONGO_DB_HOST: str
    MONGODB_PORT: str
    MONGODB_NAME: str

    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: int
    REFRESH_EXPIRE_MINUTES: int

    REDIS_HOST: str
    REDIS_PORT: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_SERVER: str
    MAIL_PORT: int

    class Config:
        env_file = Path(Path(__file__).resolve().parent.parent)/".env"


settings = Settings()



