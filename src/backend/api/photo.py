from fastapi import APIRouter, Depends, HTTPException
from backend.core.security import get_current_user
from backend.services.supabase_client import supabase

router = APIRouter()

@router.delete("/photos/{photo_id}")
async def delete_photo(photo_id: str, user = Depends(get_current_user)):
    # (1) 먼저 파일 경로만 SELECT
    sel = (
        supabase.table("photos")
        .select("file_path")
        .eq("id", photo_id)
        .eq("user_id", user.id)
        .single()
        .execute()
    )
    row = sel.data
    if not row:
        raise HTTPException(404, "Photo not found")

    file_path = row["file_path"]

    # (2) 실제 삭제 (RETURNING 은 지원 안 되므로 .single() 사용 X)
    supabase.table("photos") \
        .delete() \
        .eq("id", photo_id) \
        .eq("user_id", user.id) \
        .execute()

    # (3) 스토리지 객체도 제거
    supabase.storage.from_("photos").remove(file_path)

    return {"deleted": photo_id}

@router.patch("/photos/{photo_id}/tags")
async def update_tags(photo_id: str, new_tags: list[str],
                      user = Depends(get_current_user)):
    supabase.table("photos")\
        .update({"tags": new_tags})\
        .eq("id", photo_id).eq("user_id", user.id)\
        .execute()
    return {"ok": True}

@router.delete("/photos/{photo_id}")
async def delete_photo(photo_id: str, user=Depends(get_current_user)):
    # ① DB row 삭제
    row = supabase.table("photos")\
        .delete().eq("id", photo_id).eq("user_id", user.id)\
        .single().execute().data
    if not row:
        raise HTTPException(404, "not found")

    # ② 스토리지 객체 삭제
    supabase.storage.from_("photos").remove(row["file_path"])
    return {"deleted": photo_id}