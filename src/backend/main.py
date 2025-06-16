from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.backend.api import upload, album, duplicates, auth 

app = FastAPI()

# 라우터 등록
app.include_router(upload.router)
app.include_router(album.router)
app.include_router(duplicates.router)
app.include_router(auth.router)

# 템플릿 & 정적 파일
templates = Jinja2Templates(directory="src/backend/templates")
app.mount("/static", StaticFiles(directory="src/backend/static"), name="static")