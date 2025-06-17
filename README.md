# Smart-Photo-Sorter# 📷 Smart Photo Sorter

AI 기반의 사진 업로드 및 자동 태깅, 중복 제거, 태그 기반 검색이 가능한 웹 서비스입니다.  
Supabase를 백엔드로 활용하며, FastAPI 기반 API와 프론트엔드 JS로 구성되어 있습니다.

---

## 🌟 주요 기능

- ✅ 사진 업로드 (Drag & Drop 지원)
- ✅ AI 자동 태깅 (최대 3개)
- ✅ Supabase Storage 업로드 및 관리
- ✅ 태그 기반 검색 및 필터링
- ✅ 중복 이미지(pHash) 자동 탐지 및 삭제
- ✅ 무한 스크롤 기반 앨범 보기
- ✅ 사용자별 데이터 분리 (RLS 보안 적용)

---

## 🧠 사용 기술

| 구분 | 기술 |
|------|------|
| 백엔드 | FastAPI, Supabase (PostgREST + Storage) |
| 프론트엔드 | HTML5, Vanilla JS |
| AI 태깅 | Hugging Face 모델 API (예: `image-classification`) |
| 기타 | dotenv, uuid, hashing (SHA256 + pHash) |

---

## 📁 프로젝트 구조
Smart-Photo-Sorter/
├── src/
│   ├── backend/
│   │   ├── api/               # API 라우터 (upload, album 등)
│   │   ├── core/              # 보안, 해시 유틸 함수
│   │   ├── services/          # Supabase 및 AI 서비스 클라이언트
│   │   ├── static/            # JS, CSS 등 정적 리소스
│   │   ├── templates/         # Jinja2 HTML 템플릿
│   │   └── main.py            # FastAPI 앱 진입점
│   ├── smart_photo_sorter/    # 패키지 메타 정보
│   └── smart_photo_sorter.egg-info/
├── .env                       # 환경 변수 파일 (API 키 등)
├── requirements.txt           # 의존 패키지 목록
└── README.md

---

## ⚙️ 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/justpers/Smart-Photo-Sorter.git
cd Smart-Photo-Sorter

# 2. 가상환경 생성 및 패키지 설치
python -m venv .photo
source .photo\Scripts\activate
pip install -r requirements.txt

# 3. 환경변수 파일 설정 (.env)
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
HF_API_TOKEN=...

# 4. 서버 실행
uvicorn src.backend.main:app --reload