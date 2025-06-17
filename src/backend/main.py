from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from collections import Counter
import os
from fastapi import HTTPException

from src.backend.core.security import get_optional_current_user
from src.backend.services.supabase_client import supabase
from src.backend.api import (
    auth, upload, album as album_api, duplicates, photo  
)

app = FastAPI()

# 템플릿 / static
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.globals['env'] = os.getenv
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 메인 페이지
@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request, user=Depends(get_optional_current_user)):
    return templates.TemplateResponse("main.html", {"request": request, "user": user})

# ─── 앨범 페이지 ──────────────────────────────────────────────────────────
@app.get("/album", response_class=HTMLResponse)
async def album_page(request: Request, user=Depends(get_optional_current_user)):
    resp = (
        supabase.table("photos")
        .select("tags")
        .eq("user_id", user.id)
        .execute()
    )
    rows = resp.data or []

    flat = []
    for r in rows:
        for tag_str in (r.get("tags") or []):
            for tok in tag_str.split(","):
                tok = tok.strip()
                if tok:
                    flat.append(tok)

    counts  = Counter(flat)
    popular = [tag for tag, _ in counts.most_common(6)]

    return templates.TemplateResponse(
        "album.html",
        {
            "request": request,
            "user": user,
            "popular_tags": popular,
            "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        },
    )

# ─── 사진 상세 페이지 ─────────────────────────────────────────────────────
@app.get("/photo/{photo_id}", response_class=HTMLResponse)
async def photo_page(photo_id: str, request: Request,
                     user = Depends(get_optional_current_user)):

    cur = (
        supabase.table("photos")
        .select("*")
        .eq("id", photo_id)
        .eq("user_id", user.id)
        .single()
        .execute()
        .data
    )
    if not cur:
        raise HTTPException(404, "Photo not found")

    # ── 앨범과 똑같이 inserted_at DESC 로 정렬 ──
    rows = (
        supabase.table("photos")
        .select("id")
        .eq("user_id", user.id)
        .order("inserted_at", desc=True)   # ← 요 줄만 변경
        .execute()
        .data
    )
    id_list = [r["id"] for r in rows]
    idx     = id_list.index(photo_id)

    prev_id = id_list[idx - 1] if idx > 0 else None      # ← 왼쪽(이전 썸네일)
    next_id = id_list[idx + 1] if idx < len(id_list)-1 else None  # → 오른쪽

    return templates.TemplateResponse(
        "photo.html",
        {
            "request":      request,
            "user":         user,
            "photo":        cur,
            "prev_id":      prev_id,
            "next_id":      next_id,
            "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        },
    )

# ─── API 라우터 등록 ──────────────────────────────────────────────────────
app.include_router(auth.router,       prefix="")       # /login, /signup, /logout
app.include_router(upload.router,     prefix="/api")   # POST /api/upload
app.include_router(album_api.router,  prefix="/api")   # GET  /api/photos
app.include_router(duplicates.router, prefix="/api")   # 중복 탐색
app.include_router(photo.router,      prefix="/api")   # GET/PATCH/DELETE /api/photos/...