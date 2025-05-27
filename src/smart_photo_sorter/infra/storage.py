from pathlib import Path
from uuid import uuid4


class Storage:
    """로컬 폴더에 파일을 저장하고 경로를 반환하는 간단한 저장소 계층."""
    ROOT = Path("./uploads")
    ROOT.mkdir(exist_ok=True)

    @classmethod
    def save_file(cls, file_bytes: bytes, suffix: str = ".jpg") -> Path:
        filename = f"{uuid4()}{suffix}"
        path = cls.ROOT / filename
        path.write_bytes(file_bytes)
        return path
