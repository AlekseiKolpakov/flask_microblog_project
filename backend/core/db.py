from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from ..core.config import settings


class Base(DeclarativeBase):
    """
    Базовый класс для всех SQLAlchemy моделей.
    """

    pass


# Создаём SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO,  # логирование SQL-запросов
    future=True,
    pool_pre_ping=True,  # проверка соединения перед использованием
)


# Фабрика сессий SQLAlchemy
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Генератор SQLAlchemy-сессии.

    Используется как dependency/helper.
    Гарантирует корректное закрытие сессии.

    :return: SQLAlchemy Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
