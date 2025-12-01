import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'

load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

if not GEMINI_API_KEY:
    print("UYARI: GEMINI_API_KEY .env dosyasında bulunamadı!")