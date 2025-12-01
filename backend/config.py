import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'

load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

if not OPENAI_API_KEY:
    print("UYARI: OPENAI_API_KEY .env dosyasında bulunamadı!")