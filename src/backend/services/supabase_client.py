import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL               = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY          = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY  = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# 필수 환경변수 체크
missing = [k for k, v in {
    "SUPABASE_URL": SUPABASE_URL,
    "SUPABASE_ANON_KEY": SUPABASE_ANON_KEY,
    "SUPABASE_SERVICE_ROLE_KEY": SUPABASE_SERVICE_ROLE_KEY,
}.items() if not v]
if missing:
    raise RuntimeError(f"환경변수 누락: {', '.join(missing)}")

# ────────────────────────────────────
# 1) 읽기·인증 확인용 (anon 키)
supabase_anon = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# 2) 쓰기·업로드 전용 (service-role 키)  ← RLS 우회
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)