import os
from dotenv import load_dotenv

load_dotenv()

# === TELEGRAM ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_USER_ID = int(os.getenv("OWNER_USER_ID", "0"))

# === GEMINI ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash-8b"

# === SUPABASE ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# === CLOUDFLARE R2 ===
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "javix-files")
R2_ENDPOINT = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

# === XAVFSIZLIK ===
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# === SOZLAMALAR ===
MAX_VOICE_DURATION = 300
MAX_FILE_SIZE = 20 * 1024 * 1024
CONTEXT_MESSAGES = 20
TIMEZONE = "Asia/Tashkent"

# === TIL ===
SUPPORTED_LANGUAGES = ["uz", "ru", "en"]
DEFAULT_LANGUAGE = "uz"
