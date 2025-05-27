from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List

from .tag import Tag


@dataclass
class Photo:
    photo_id: str
    file_path: Path
    status: str
    upload_date: datetime
    hash_value: str
    tags: List[Tag] = field(default_factory=list)

    def attach_tags(self, tags: List[Tag]) -> None:
        self.tags.extend(tags)
        self.status = "Tagged"