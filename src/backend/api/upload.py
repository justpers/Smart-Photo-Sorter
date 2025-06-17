from typing import List
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from backend.core.security import get_current_user
from backend.services.supabase_client import supabase  # ← admin 클라이언트
import uuid, logging
from urllib.parse import quote

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.post("/upload")
async def upload_images(
    files: List[UploadFile] = File(...),
    user = Depends(get_current_user)
):
    saved_keys = []
    for file in files:
        safe_name = quote(file.filename, safe="._-")
        key = f"{user.id}/{uuid.uuid4().hex}_{safe_name}"
        data = await file.read()

        # Storage 업로드 (service-role 키이므로 RLS 우회)
        try:
            supabase.storage.from_("photos").upload(key, data)
        except Exception as e:
            logger.error(f"Storage upload failed ({file.filename}): {e}", exc_info=True)
            raise HTTPException(500, f"Storage 업로드 실패: {file.filename}")

        saved_keys.append(key)

    # 여러 행 한꺼번에 INSERT
    rows = [{"user_id": user.id, "file_path": k, "tags": []} for k in saved_keys]
    try:
        supabase.table("photos").insert(rows).execute()
    except Exception as e:
        logger.error(f"DB insert failed: {e}", exc_info=True)
        raise HTTPException(500, "DB 기록 실패")

    return JSONResponse({"status": "ok", "files": saved_keys})