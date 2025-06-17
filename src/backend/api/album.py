from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from backend.core.security import get_current_user
from backend.services.supabase_client import supabase

router = APIRouter()

@router.get("/photos")
async def list_photos(
    tag: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    user = Depends(get_current_user),
):
    # 기본 쿼리: 로그인된 사용자의 사진
    query = supabase.table("photos").select("*").eq("user_id", user.id)
    if tag:
        query = query.contains("tags", [tag])
    query = query.order("inserted_at", desc=True).range(offset, offset + limit - 1)

    resp = query.execute()
    photos = resp.data or []

    # 전체 카운트 조회
    count_res = supabase.table("photos") \
        .select("id", count="exact", head=True) \
        .eq("user_id", user.id) \
        .execute()
    total = count_res.count or 0

    return JSONResponse({"photos": photos, "count": total})