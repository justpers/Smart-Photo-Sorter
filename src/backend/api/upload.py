from typing import List
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from backend.core.security import get_current_user
from backend.services.supabase_client import supabase  # ← admin 클라이언트
from backend.services.ai_service import AIService
import uuid, logging
from urllib.parse import quote
import anyio

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.post("/upload")
async def upload_images(
    files: List[UploadFile] = File(...),
    user = Depends(get_current_user)
):
    saved = []
    for f in files:
        data = await f.read()
        safe = quote(f.filename, safe="._-")
        key  = f"{user.id}/{uuid.uuid4().hex}_{safe}"

        # 1) 스토리지에 업로드
        try:
            supabase.storage.from_("photos").upload(key, data)
        except Exception as e:
            logger.error("Storage upload failed", exc_info=True)
            raise HTTPException(500, f"Storage 업로드 실패: {f.filename}")

        # 2) AI 태그 생성 (블로킹 호출을 스레드풀에서 실행)
        try:
            tags = await anyio.to_thread.run_sync(
                AIService.generate_tags_bytes, data, 3
            )
        except Exception as e:
            logger.warning("AI 태깅 실패, 빈 태그 반환", exc_info=True)
            tags = []

        saved.append({"file_path": key, "tags": [t.name for t in tags]})

    # 3) DB에 일괄 INSERT (tags → text[] 컬럼)
    rows = [
        {"user_id": user.id, "file_path": x["file_path"], "tags": x["tags"]}
        for x in saved
    ]
    try:
        supabase.table("photos").insert(rows).execute()
    except Exception as e:
        logger.error("DB 기록 실패", exc_info=True)
        raise HTTPException(500, "DB 기록 실패")

    return JSONResponse({"status":"ok","files": saved})