from typing import List
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from backend.core.security import get_current_user
from backend.services.supabase_client import supabase  # Service Role 키 클라이언트
from backend.services.ai_service import AIService
from backend.core.hash_utils import calc_hashes
from urllib.parse import quote
import uuid, logging

router = APIRouter()
logger = logging.getLogger("uvicorn.error")


@router.post("/upload")
async def upload_images(
    files: List[UploadFile] = File(...),
    user = Depends(get_current_user)
):
    """
    1) SHA256 + pHash 계산
    2) Supabase Storage 업로드 (service-role)
    3) AI 태깅 → 최대 3개 토큰
    4) Supabase Table("photos")에 INSERT (service-role)
    """
    to_insert = []

    for f in files:
        # 안전한 파일명 생성
        safe_name = quote(f.filename, safe="._-")
        key       = f"{user.id}/{uuid.uuid4().hex}_{safe_name}"
        data      = await f.read()

        # 1) 해시 계산
        try:
            sha256, phash = calc_hashes(data)
        except Exception as e:
            logger.warning(f"Hash 계산 실패 ({f.filename}): {e}", exc_info=True)
            sha256, phash = None, None

        # 2) Storage 업로드
        try:
            supabase.storage.from_("photos").upload(key, data)
        except Exception as e:
            logger.error("Storage 업로드 실패", exc_info=True)
            raise HTTPException(500, f"Storage 업로드 실패: {f.filename}")

        # 3) AI 태깅
        try:
            preds = AIService._query(data, top_k=3)
        except Exception as e:
            logger.error("AI 태깅 실패", exc_info=True)
            preds = []

        seen, tokens = set(), []
        for p in preds:
            for tok in p.get("label", "").split(","):
                tok = tok.strip()
                if tok and tok not in seen:
                    seen.add(tok)
                    tokens.append(tok)
                if len(tokens) >= 3:
                    break
            if len(tokens) >= 3:
                break

        # 4) DB INSERT 준비
        to_insert.append({
            "user_id": user.id,
            "file_path": key,
            "tags": tokens,
            "sha256": sha256,
            "phash": phash,
        })

    # 4) Supabase 테이블에 한 번에 INSERT
    try:
        supabase.table("photos").insert(to_insert).execute()
    except Exception as e:
        logger.error("DB INSERT 실패", exc_info=True)
        raise HTTPException(500, "DB 기록 실패")

    return JSONResponse({
        "status": "ok",
        "files": [row["file_path"] for row in to_insert]
    })