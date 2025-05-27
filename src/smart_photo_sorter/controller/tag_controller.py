from smart_photo_sorter.entity.photo import Photo
from smart_photo_sorter.service.ai_service import AIService


class TagController:
    """자동 태깅 담당 Controller"""

    @staticmethod
    def auto_tag(photo: Photo) -> None:
        tags = AIService.generate_tags(photo)
        photo.attach_tags(tags)