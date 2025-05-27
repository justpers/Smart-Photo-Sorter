"""
AIService – Hugging Face Inference API 기반 이미지 자동 태깅

모델  : microsoft/resnet-50   (pipeline: image-classification, multi-label 지원)
입력  : 이미지 바이너리(예: JPEG/PNG)
출력  : 상위 top_k개의 라벨·신뢰도 → Tag 객체 List
"""

from __future__ import annotations
import os
import requests
from typing import List

from smart_photo_sorter.entity.photo import Photo
from smart_photo_sorter.entity.tag import Tag

# ── 환경변수에서 API 토큰 읽기 ───────────────────────────
HF_TOKEN = os.getenv("HF_API_TOKEN")
if HF_TOKEN is None:
    raise RuntimeError(
        "환경변수 HF_API_TOKEN이 설정되지 않음"
    )

MODEL_ID = "microsoft/resnet-50"
API_URL  = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS  = {"Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/octet-stream"
        }


class AIService:
    """Hugging Face Inference API로부터 상위 K개 이미지 태그를 받아오는 서비스"""

    @staticmethod
    def _query(image_bytes: bytes, top_k: int = 5) -> list[dict]:
        
        if not image_bytes:
            raise ValueError("이미지 데이터가 비어 있습니다.")
        response = requests.post(
            API_URL,
            headers=HEADERS,
            data=image_bytes,
            timeout=30,
        )
        print("응답 상태코드:", response.status_code)
        print("응답 내용:", response.text[:300])  # 앞부분만 출력
        response.raise_for_status()

        # API가 모델 로딩 중이면 503 반환 → 재시도 권장
        if response.status_code == 503:
            raise RuntimeError("모델 로딩 중입니다. 잠시 후 다시 시도하세요.")
        response.raise_for_status()
        # 예: [{'score': 0.95, 'label': 'German shepherd'}, ...]
        return response.json()[:top_k]

    # ────────────────────────────────────────────────────────
    @classmethod
    def generate_tags(cls, photo: Photo, top_k: int = 3) -> List[Tag]:
        """Photo -> Tag List (상위 top_k)"""
        with open(photo.file_path, "rb") as f:
            predictions = cls._query(f.read(), top_k=max(top_k, 1))

        tags: list[Tag] = []
        for pred in predictions:
            label: str = pred["label"]
            confidence: float = round(float(pred["score"]), 2)
            # 간단 분류: 첫 단어를 category 로 지정
            category = label.split()[0]
            tags.append(Tag(name=label, category=category, confidence=confidence))
        return tags