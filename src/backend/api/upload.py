from typing import List
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from backend.core.security import get_current_user
from backend.services.supabase_client import supabase  # ← admin 클라이언트
from backend.services.ai_service import AIService
import uuid, logging
from urllib.parse import quote

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.post("/upload")
async def upload_images(
    files: List[UploadFile] = File(...),
    user = Depends(get_current_user)
):
    saved = []   # [(key, [tag_tokens])]
    for f in files:
        safe_name = quote(f.filename, safe="._-")
        key       = f"{user.id}/{uuid.uuid4().hex}_{safe_name}"
        data      = await f.read()

        # 1) 스토리지 업로드
        try:
            supabase.storage.from_("photos").upload(key, data)
        except Exception as e:
            logger.error("Storage upload failed:", exc_info=True)
            raise HTTPException(500, f"Storage 업로드 실패: {f.filename}")

        # 2) HF API 로 태그 예측 → [{label,score},…]
        try:
            preds = AIService._query(data, top_k=5)
        except Exception as e:
            logger.error("AI tagging failed:", exc_info=True)
            preds = []

        # 3) 라벨 문자열을 쉼표로 분할 → 토큰 리스트
        tokens = []
        for p in preds:
            for tok in p["label"].split(","):
                tok = tok.strip()
                if tok:
                    tokens.append(tok)

        saved.append((key, tokens))

    # 4) DB 에 한 번에 insert
    rows = [
        {"user_id": user.id, "file_path": key, "tags": tags}
        for key, tags in saved
    ]
    try:
        supabase.table("photos").insert(rows).execute()
    except Exception as e:
        logger.error("DB insert failed:", exc_info=True)
        raise HTTPException(500, "DB 기록 실패")

    return JSONResponse({"status":"ok","files":[k for k,_ in saved]})