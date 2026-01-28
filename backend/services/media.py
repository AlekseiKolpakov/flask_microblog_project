import os
from uuid import uuid4

from sqlalchemy.orm import Session

from ..models.media import Media

# Директория для хранения загруженных файлов
UPLOAD_DIR = "uploads"


def save_media(
    db: Session,
    file,
    owner_id: int,
) -> Media:
    """
    Сохранить медиафайл на диск и записать его в базу данных.

    Файл сохраняется с уникальным именем,
    чтобы избежать конфликтов.

    :param db: SQLAlchemy сессия
    :param file: Загруженный файл (werkzeug FileStorage)
    :param owner_id: ID пользователя — владельца файла
    :return: Объект Media
    """
    # Создаём директорию, если она не существует
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Генерирует уникальное имя файла
    filename = f"{uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Сохраняем файл на диск
    file.save(file_path)

    # Создаём запись в базе данных
    media = Media(
        url=f"/uploads/{filename}",
        owner_id=owner_id,
    )

    db.add(media)
    db.commit()
    db.refresh(media)

    return media
