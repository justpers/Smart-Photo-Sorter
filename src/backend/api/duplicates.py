from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from backend.core.security import get_current_user
from backend.services.supabase_client import supabase
import imagehash, collections, logging

logger = logging.getLogger("uvicorn.error")
router = APIRouter(prefix="/duplicates", tags=["duplicates"])
HAMMING_THRESHOLD = 6  # 필요에 따라 조정

def _hex_to_hash(hexstr: str):
    return imagehash.hex_to_hash(hexstr)

@router.get("/", response_model=List[List[str]])
async def list_duplicates(user=Depends(get_current_user)):
    """
    GET /api/duplicates
    SHA-256 완전 일치 그룹과 pHash 유사 그룹을 반환합니다.
    """
    try:
        resp = (
            supabase
              .table("photos")
              .select("id,sha256,phash")
              .eq("user_id", user.id)
              .execute()
        )
        photos = resp.data or []
    except Exception as e:
        logger.error(f"중복 조회 예외: {e}", exc_info=True)
        raise HTTPException(500, "중복 조회 중 에러가 발생했습니다.")

    # 1) SHA-256 기반 완전 일치
    sha_buckets = collections.defaultdict(list)
    for p in photos:
        sha = p.get("sha256")
        if sha:
            sha_buckets[sha].append(p["id"])
    exact = [group for group in sha_buckets.values() if len(group) > 1]

    # 2) pHash 기반 근사 일치
    ph_buckets = collections.defaultdict(list)
    for p in photos:
        ph = p.get("phash")
        if ph:
            ph_buckets[ph[:4]].append(p)

    near = []
    visited = set()
    for bucket in ph_buckets.values():
        for base in bucket:
            bid, bph = base["id"], base["phash"]
            if not bph or bid in visited:
                continue

            group = [bid]
            h0 = _hex_to_hash(bph)
            for other in bucket:
                oid, oph = other["id"], other.get("phash")
                if oid == bid or oid in visited or not oph:
                    continue
                if (_hex_to_hash(oph) - h0) <= HAMMING_THRESHOLD:
                    group.append(oid)
                    visited.add(oid)

            if len(group) > 1:
                near.append(group)

    return exact + near


class ResolveBody(BaseModel):
    keep_id: str
    delete_ids: List[str]


@router.post("/resolve")
async def resolve_duplicates(
    body: ResolveBody,
    user=Depends(get_current_user)
):
    """
    POST /api/duplicates/resolve
    keep_id를 제외한 delete_ids를 Storage와 DB에서 삭제합니다.
    """
    if body.keep_id in body.delete_ids:
        raise HTTPException(400, "keep_id가 delete_ids에 포함될 수 없습니다.")

    # 1) 삭제 대상 file_path 조회
    try:
        resp = (
            supabase
              .table("photos")
              .select("file_path")
              .in_("id", body.delete_ids)
              .eq("user_id", user.id)
              .execute()
        )
        rows = resp.data or []
    except Exception as e:
        logger.error(f"삭제 대상 조회 예외: {e}", exc_info=True)
        raise HTTPException(500, "삭제 대상 조회 실패")

    paths = [r["file_path"] for r in rows]
    if not paths:
        # 삭제할 게 없으면 바로 리턴
        return {"deleted": 0}

    # 2) Storage에서 파일 삭제
    try:
        supabase.storage.from_("photos").remove(paths)
    except Exception as e:
        logger.error(f"Storage 삭제 예외: {e}", exc_info=True)
        raise HTTPException(500, "Storage 삭제 실패")

    # 3) DB 레코드 삭제
    try:
        supabase \
          .table("photos") \
          .delete() \
          .in_("id", body.delete_ids) \
          .eq("user_id", user.id) \
          .execute()
    except Exception as e:
        logger.error(f"DB 삭제 예외: {e}", exc_info=True)
        raise HTTPException(500, "DB 삭제 실패")

    return {"deleted": len(paths)}