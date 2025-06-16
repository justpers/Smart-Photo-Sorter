from fastapi import Request, HTTPException
from backend.services.supabase_client import supabase

def get_current_user(request: Request):
    """
    로그인 필수: Request 객체에서 쿠키를 꺼내고, 
    supabase.auth.get_user()로 검증. 실패 시 HTTPException(401).
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    res = supabase.auth.get_user(token)
    user = getattr(res, "user", None) or res.data.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

def get_optional_current_user(request: Request):
    """
    로그인했으면 user, 아니면 None. 에러 없이 넘어감.
    """
    token = request.cookies.get("access_token")
    if not token:
        return None
    res = supabase.auth.get_user(token)
    return getattr(res, "user", None) or res.data.get("user")