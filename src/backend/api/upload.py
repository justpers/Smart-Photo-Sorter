from typing import List
from urllib.parse import quote
import uuid, logging

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse

from backend.core.security   import get_current_user
from backend.core.hash_utils import calc_hashes
from backend.services.ai_service import AIService

# 분리된 Supabase 클라이언트 가져오기
from backend.services.supabase_client import supabase_admin as supabase
router = APIRouter()
logger = logging.getLogger("uvicorn.error")


@router.post("/upload")
async def upload_images(
    files: List[UploadFile] = File(...),
    user = Depends(get_current_user)
):

    if not files:
        raise HTTPException(400, "업로드할 파일이 없습니다.")

    rows_to_insert = []

    for f in files:
        safe_name = quote(f.filename, safe="._-")
        key       = f"{user.id}/{uuid.uuid4().hex}_{safe_name}"
        data      = await f.read()

        try:
            sha256, phash = calc_hashes(data)
        except Exception as e:
            logger.warning(f"Hash 계산 실패 ({f.filename}): {e}", exc_info=True)
            sha256, phash = None, None

        try:
            supabase.storage.from_("photos").upload(key, data, {
                "content-type": f.content_type or "application/octet-stream"
            })
        except Exception as e:
            logger.error("Storage 업로드 실패", exc_info=True)
            raise HTTPException(500, f"Storage 업로드 실패: {f.filename}")

        try:
            preds = AIService._query(data, top_k=3)
        except Exception as e:
            logger.error("AI 태깅 실패", exc_info=True)
            preds = []

        tags, seen = [], set()
        for p in preds:
            for tok in p.get("label", "").split(","):
                tok = tok.strip()
                if tok and tok not in seen:
                    seen.add(tok)
                    tags.append(tok)
                if len(tags) >= 3:
                    break
            if len(tags) >= 3:
                break

        rows_to_insert.append({
            "user_id"  : user.id,
            "file_path": key,
            "tags"     : tags,
            "sha256"   : sha256,
            "phash"    : phash,
        })

    try:
        supabase.table("photos").insert(rows_to_insert).execute()
    except Exception as e:
        logger.error("DB INSERT 실패", exc_info=True)
        raise HTTPException(500, "DB 기록 실패")

    return JSONResponse({
        "status": "ok",
        "files": [row["file_path"] for row in rows_to_insert]
    })