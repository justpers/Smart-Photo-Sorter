from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()  

templates = Jinja2Templates(directory="src/backend/templates")

@router.get("/duplicates", response_class=HTMLResponse)
def view_duplicates(request: Request):
    return templates.TemplateResponse("duplicates.html", {"request": request})