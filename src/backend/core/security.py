from fastapi import Request, HTTPException
from gotrue.errors import AuthApiError
from backend.services.supabase_client import supabase_anon

def get_current_user(request: Request):
    """
    로그인 필수:
    - access_token 쿠키가 없으면 401
    - 토큰 검증 실패 (만료·잘못된 토큰)이면 401
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        res = supabase_anon.auth.get_user(token)
    except AuthApiError:
        # 만료되었거나 서명 불일치 등
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = getattr(res, "user", None) or res.data.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user

def get_optional_current_user(request: Request):
    """
    로그인했으면 User, 아니면 None.
    - 토큰 없거나 만료·오류 시에도 None 반환
    """
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        res = supabase_anon.auth.get_user(token)
        return getattr(res, "user", None) or res.data.get("user")
    except AuthApiError:
        return None