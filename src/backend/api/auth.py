from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.services.supabase_client import supabase
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="src/backend/templates")

# ---------- 회원가입 ----------
@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def signup(request: Request, email: str = Form(...), password: str = Form(...)):
    res = supabase.auth.sign_up({"email": email, "password": password})
    if res.user:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("signup.html", {"request": request, "error": "회원가입 실패"})

# ---------- 로그인 ----------
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if res.session:
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key="access_token", value=res.session.access_token, httponly=True)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "로그인 실패"})

# ---------- 로그아웃 ----------
@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
