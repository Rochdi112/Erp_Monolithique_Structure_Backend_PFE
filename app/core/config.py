# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "ERP Interventions"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # durée de validité JWT en minutes

    # Email SMTP
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: str

    # Base de données PostgreSQL
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: str = "5432"

    # Répertoire d’upload de fichiers
    UPLOAD_DIRECTORY: str = Field(default="app/static/uploads")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"  # empêche l’utilisation de variables non déclarées


settings = Settings()
