import uuid
import logging
from urllib.parse import quote
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from backend.core.security import get_current_user
from backend.services.supabase_client import supabase
from pathlib import Path

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):
    # 1) 파일 확장자만 가져오기
    ext = Path(file.filename).suffix   # e.g. ".png", ".jpg"
    # 2) UUID 기반의 완전 안전한 키 생성
    key = f"{user.id}/{uuid.uuid4().hex}{ext}"
    data = await file.read()

    try:
        supabase.storage.from_("photos").upload(key, data)
    except Exception as e:
        logger.error(f"Storage upload failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Storage 업로드 실패: {e}")

    try:
        supabase.table("photos").insert({
            "user_id": user.id,
            "file_path": key,
            "tags": []
        }).execute()
    except Exception as e:
        logger.error(f"DB insert failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"DB 기록 실패: {e}")

    return JSONResponse({"status":"ok","filePath": key})