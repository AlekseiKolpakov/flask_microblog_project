import os
from uuid import uuid4

from sqlalchemy.orm import Session

from ..models.media import Media

UPLOAD_DIR = "uploads"


def save_media(
    db: Session,
    file,
    owner_id: int,
) -> Media:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    file.save(file_path)

    media = Media(
        url=f"/uploads/{filename}",
        owner_id=owner_id,
    )

    db.add(media)
    db.commit()
    db.refresh(media)

    return media
