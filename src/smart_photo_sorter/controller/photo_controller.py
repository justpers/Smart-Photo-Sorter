from smart_photo_sorter.controller.photo_manager import PhotoManager
from smart_photo_sorter.controller.tag_controller import TagController
from smart_photo_sorter.entity.user import User


class PhotoController:
    """GRASP Controller – 사진 업로드 UC 총괄"""

    def __init__(self) -> None:
        self.photo_manager = PhotoManager()
        self.tag_controller = TagController()

    def upload(self, user: User, photo_bytes: bytes, meta: dict) -> str:
        photo = self.photo_manager.store(photo_bytes, meta)
        user.add_photo(photo)
        # include UC: 자동 태깅
        self.tag_controller.auto_tag(photo)
        return photo.photo_id