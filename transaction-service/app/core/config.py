import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(".env")


class Config(BaseSettings):
    APP_NAME: str = "transaction-service"

    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL")

    SECRET_KEY: str = os.getenv("SECRET_KEY")

    DB_ENGINE: str = os.getenv("DB_ENGINE", "postgresql")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_DATABASE: str = os.getenv("DB_DATABASE")

    DATABASE_URI: str = (
        "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
            db_engine=DB_ENGINE,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE,
        )
    )


config = Config()
