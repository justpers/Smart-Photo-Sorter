from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

# 페이지 핸들러
from src.backend.core.security import get_optional_current_user
# API 라우터
from src.backend.api import auth, upload, album as album_api, duplicates

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

# 앨범 페이지
@app.get("/album", response_class=HTMLResponse)
async def album_page(request: Request, user=Depends(get_optional_current_user)):
    # TODO: 실제 DB에서 top 6 태그를 뽑아주세요.
    popular = ["apron", "food market", "dog", "travel", "flower", "sunset"]
    return templates.TemplateResponse(
        "album.html",
        {
            "request": request,
            "user": user,
            "popular_tags": popular,
            "SUPABASE_URL": os.getenv("SUPABASE_URL")
        }
    )

# API 라우터 (prefix="/api")
app.include_router(auth.router,       prefix="")       # /login, /signup, /logout
app.include_router(upload.router,     prefix="/api")    # POST /api/upload
app.include_router(album_api.router,  prefix="/api")    # GET  /api/photos
app.include_router(duplicates.router, prefix="/api")    # e.g. GET /api/duplicates