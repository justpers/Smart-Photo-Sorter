from pathlib import Path

from smart_photo_sorter.controller.photo_controller import PhotoController
from smart_photo_sorter.entity.user import User


class PhotoUploadUI:
    """CLI용 간단 Boundary"""

    def __init__(self, controller: PhotoController) -> None:
        self.controller = controller

    def select_photo(self, user: User, filepath: str) -> None:
        with open(filepath, "rb") as f:
            photo_id = self.controller.upload(
                user=user,
                photo_bytes=f.read(),
                meta={"filename": Path(filepath).name},
            )
        self.show_confirmation(photo_id)

    @staticmethod
    def show_confirmation(photo_id: str) -> None:
        print(f"[UI] 업로드 완료! photoId = {photo_id}")