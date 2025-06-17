"""
AIService – Hugging Face Inference API 기반 이미지 자동 태깅

모델  : microsoft/resnet-50   (pipeline: image-classification, multi-label 지원)
입력  : 이미지 바이너리(예: JPEG/PNG)
출력  : 상위 top_k개의 라벨·신뢰도 → Tag 객체 List
"""
import os
import requests
from typing import List
from smart_photo_sorter.entity.tag import Tag

HF_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("환경변수 HF_API_TOKEN이 설정되지 않음")

MODEL_ID = "microsoft/resnet-50"
API_URL  = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS  = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/octet-stream",
}

class AIService:
    @staticmethod
    def _query(image_bytes: bytes, top_k: int = 3) -> list[dict]:
        if not image_bytes:
            raise ValueError("이미지 데이터가 비어 있습니다.")
        resp = requests.post(API_URL, headers=HEADERS, data=image_bytes, timeout=30)
        resp.raise_for_status()
        # top_k 만큼 자르기
        return resp.json()[:top_k]

    @classmethod
    def generate_tags_bytes(cls, image_bytes: bytes, top_k: int = 3) -> List[Tag]:
        preds = cls._query(image_bytes, top_k=max(top_k, 1))
        tags: list[Tag] = []
        for p in preds:
            label = p["label"]
            score = round(float(p["score"]), 2)
            category = label.split()[0]
            tags.append(Tag(name=label, category=category, confidence=score))
        return tags