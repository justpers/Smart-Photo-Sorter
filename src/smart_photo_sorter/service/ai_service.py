import random
from typing import List

from smart_photo_sorter.entity.photo import Photo
from smart_photo_sorter.entity.tag import Tag


class AIService:
    """더미 AI 태깅 서비스."""
    SAMPLE_TAGS = [
        ("cat", "animal"), ("dog", "animal"),
        ("beach", "place"), ("sunset", "time"),
        ("portrait", "style"),
    ]

    @classmethod
    def generate_tags(cls, photo: Photo) -> List[Tag]:
        chosen = random.sample(cls.SAMPLE_TAGS, k=3)
        return [
            Tag(name=n, category=c, confidence=round(random.uniform(0.7, 0.99), 2))
            for n, c in chosen
        ]