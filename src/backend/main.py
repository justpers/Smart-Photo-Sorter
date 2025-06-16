from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# 라우터들
from src.backend.api import upload, album, duplicates, auth  # upload.router 은 이제 /가 아님
from src.backend.core.security import get_optional_current_user

app = FastAPI()

# --- 템플릿 & Static 설정 ---
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# --- 메인 페이지 핸들러 (/ root) ---
@app.get("/", response_class=HTMLResponse)
async def main_page(
    request: Request,
    user = Depends(get_optional_current_user)
):
    # 쿼리스트링 플래그를 템플릿에 넘기기
    params = dict(request.query_params)
    return templates.TemplateResponse("main.html", {
        "request": request,
        "user": user,
        "login_error": params.get("login_error"),
        "signup_error": params.get("signup_error"),
    })

# --- 다른 라우터 등록 ---
app.include_router(auth.router)            # /login, /signup, /logout
app.include_router(album.router, prefix="") # /album
app.include_router(duplicates.router, prefix="")  # /duplicates
app.include_router(upload.router)