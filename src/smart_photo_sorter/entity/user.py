from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from .photo import Photo


@dataclass
class User:
    user_id: str
    email: str
    name: str
    photos: List[Photo] = field(default_factory=list)

    def add_photo(self, photo: Photo) -> None:
        self.photos.append(photo)