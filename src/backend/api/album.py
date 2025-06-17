from typing import Optional
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
    if not (1 <= limit <= 100):
        raise HTTPException(400, "limit 파라미터는 1~100이어야 합니다.")

    # ── (1) 목록 조회 ───────────────────────────────────────────────
    list_q = (
        supabase.table("photos")
        .select("*")
        .eq("user_id", user.id)
    )
    if tag:
        list_q = list_q.contains("tags", [tag])

    photos_resp = (
        list_q
        .order("inserted_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    photos = photos_resp.data or []

    # ── (2) 동일 조건으로 전체 개수 조회 ────────────────────────────
    count_q = (
        supabase.table("photos")
        .select("id", count="exact", head=True)   # head=True → 행 데이터 생략
        .eq("user_id", user.id)
    )
    if tag:
        count_q = count_q.contains("tags", [tag])

    total = (count_q.execute().count) or 0

    return JSONResponse({"photos": photos, "count": total})