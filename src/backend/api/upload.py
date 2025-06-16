from fastapi import APIRouter, UploadFile, File, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.services.supabase_client import supabase
from backend.core.security import get_current_user, get_optional_current_user
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="src/backend/templates")

@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request, user=Depends(get_optional_current_user)):
    return templates.TemplateResponse("main.html", {
        "request": request,
        "user": user
    })

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    user=Depends(get_current_user)                 # ← 로그인 필수
):
    filename = f"{user.id}/{uuid.uuid4()}_{file.filename}"
    # 1) Storage 업로드
    supabase.storage.from_("photos").upload(f"photos/{filename}", await file.read(), upsert=True)
    # 2) DB 저장 (user_id 포함)
    supabase.table("photos").insert({
        "user_id": user.id,
        "file_path": f"photos/{filename}",
        "tags": [],
    }).execute()
    return {"message": "Upload successful"}