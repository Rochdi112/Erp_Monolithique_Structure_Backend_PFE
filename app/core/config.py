# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "ERP Interventions"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = Field(default="insecure-test-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # durée de validité JWT en minutes

    # Email SMTP
    SMTP_HOST: str = Field(default="localhost")
    SMTP_PORT: int = Field(default=1025)  # Mailhog/Mailcatcher default
    SMTP_USER: str = Field(default="user")
    SMTP_PASSWORD: str = Field(default="password")
    EMAILS_FROM_EMAIL: str = Field(default="no-reply@example.com")

    # Base de données PostgreSQL
    POSTGRES_DB: str = Field(default="app")
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: str = "5432"

    # Répertoire d’upload de fichiers
    UPLOAD_DIRECTORY: str = Field(default="app/static/uploads")

    # Pydantic v2 settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",  # empêche l’utilisation de variables non déclarées
    )


settings = Settings()
