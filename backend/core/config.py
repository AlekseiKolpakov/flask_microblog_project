from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Глобальные настройки приложения.

    Значения берутся из переменных окружения или файла `.env`.
    Используется Pydantic для валидации и типизации.
    """

    # Режим работы приложения: dev или prod
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    # URL подключения к базе данных
    DATABASE_URL: str = "sqlite:///./app.db"

    # Включение режима отладки Flask
    DEBUG: bool = False

    # Логирование SQL-запросов SQLAlchemy
    SQL_ECHO: bool = False

    # Конфигурация Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # игнорируем лишние переменные окружения
    )


# Глобальный объект настроек
settings = Settings()
