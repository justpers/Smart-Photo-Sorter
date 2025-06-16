from typing import List
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from backend.core.security import get_current_user
from backend.services.supabase_client import supabase
import uuid
from urllib.parse import quote
import logging

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.post("/upload")
async def upload_images(
    files: List[UploadFile] = File(...),      # ← 여기를 List[UploadFile]
    user = Depends(get_current_user)
):
    saved_keys = []
    for file in files:
        # URL‐safe 파일명
        safe_name = quote(file.filename, safe="._-")
        key = f"{user.id}/{uuid.uuid4().hex}_{safe_name}"
        data = await file.read()

        try:
            supabase.storage.from_("photos").upload(key, data)
        except Exception as e:
            logger.error(f"Storage upload failed ({file.filename}): {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Storage 업로드 실패: {file.filename}")

        saved_keys.append(key)

    # 2) 한 번에 DB에 여러 rows 삽입
    rows = [{"user_id": user.id, "file_path": key, "tags": []} for key in saved_keys]
    try:
        supabase.table("photos").insert(rows).execute()
    except Exception as e:
        logger.error(f"DB insert failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="DB 기록 실패")

    return JSONResponse({"status":"ok","files": saved_keys})