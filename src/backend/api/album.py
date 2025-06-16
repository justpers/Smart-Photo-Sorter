from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter() 

templates = Jinja2Templates(directory="src/backend/templates")

@router.get("/album", response_class=HTMLResponse)
def view_album(request: Request):
    return templates.TemplateResponse("album.html", {"request": request})