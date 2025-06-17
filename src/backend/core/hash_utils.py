from io import BytesIO
from typing import Tuple

from PIL import Image
import imagehash                    # pHash 구현
import hashlib

HASH_SIZE = 8        # 8×8 DCT ⇒ 64-bit pHash

def calc_hashes(raw: bytes) -> Tuple[str, str]:
    """
    반환값: (sha256, phash_hex)
    sha256  : 완전 동일 이미지 판별
    phash   : 시각적 유사 이미지 판별
    """
    sha = hashlib.sha256(raw).hexdigest()
    phash = imagehash.phash(Image.open(BytesIO(raw)),
                            hash_size=HASH_SIZE)
    return sha, str(phash)          # hexfmt