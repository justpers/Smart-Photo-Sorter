from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.services.supabase_client import supabase
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="src/backend/templates")

@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}_{file.filename}"
    supabase.storage.from_("photos").upload(f"photos/{filename}", await file.read(), upsert=True)
    supabase.table("photos").insert({
        "file_path": f"photos/{filename}",
        "tags": [],
    }).execute()
    return {"message": "Upload successful"}
