from datetime import datetime
from uuid import uuid4

from smart_photo_sorter.entity.photo import Photo
from smart_photo_sorter.infra.storage import Storage


class PhotoManager:
    """사진을 저장하고 Photo 엔티티를 생성(Creator)"""

    @staticmethod
    def store(photo_bytes: bytes, meta: dict) -> Photo:
        photo_id = str(uuid4())
        file_path = Storage.save_file(photo_bytes, suffix=".jpg")
        return Photo(
            photo_id=photo_id,
            file_path=file_path,
            status="Uploaded",
            upload_date=datetime.now(),
            hash_value="dummyhash",
            tags=[],
        )