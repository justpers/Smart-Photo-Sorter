from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from gotrue.errors import AuthApiError
from backend.services.supabase_client import supabase

router = APIRouter()

@router.get("/login")
async def login_get():
    return RedirectResponse("/", 302)

@router.get("/signup")
async def signup_get():
    return RedirectResponse("/", 302)

@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    except AuthApiError:
        return RedirectResponse("/?login_error=1", 302)
    if getattr(res, "session", None):
        resp = RedirectResponse("/?login_success=1", 302)
        resp.set_cookie("access_token", res.session.access_token, httponly=True, samesite="lax")
        return resp
    return RedirectResponse("/?login_error=1", 302)


@router.post("/signup")
async def signup(email: str = Form(...), password: str = Form(...)):
    # 1) 계정 생성
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
    except AuthApiError:
        return RedirectResponse("/?signup_error=1", 302)

    # 2) 가입 성공하면 즉시 로그인 시도
    if getattr(res, "user", None):
        try:
            login_res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        except AuthApiError:
            # 로그인 실패해도, 가입은 된 상태이므로 signup_success 플래그만
            return RedirectResponse("/?signup_success=1", 302)

        if getattr(login_res, "session", None):
            # 로그인 성공: 쿠키 세팅 + 로그인 성공 플래그
            resp = RedirectResponse("/?login_success=1", 302)
            resp.set_cookie("access_token", login_res.session.access_token, httponly=True, samesite="lax")
            return resp

        # (비록 세션 획득 실패해도) 가입 성공 플래그로 돌아가기
        return RedirectResponse("/?signup_success=1", 302)

    # 가입 실패
    return RedirectResponse("/?signup_error=1", 302)


@router.get("/logout")
async def logout():
    resp = RedirectResponse("/", 302)
    resp.delete_cookie("access_token")
    return resp