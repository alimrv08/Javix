from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_SERVICE_KEY
from security.encryption import encrypt, decrypt
from datetime import datetime
import pytz
from config import TIMEZONE

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
tz = pytz.timezone(TIMEZONE)


# ──────────────────────────────────────────
#  SUHBAT TARIXI
# ──────────────────────────────────────────

def save_message(user_id: int, role: str, content: str):
    """Xabarni shifrlangan holda saqlaydi."""
    supabase.table("messages").insert({
        "user_id": user_id,
        "role": role,
        "content": encrypt(content),
        "created_at": datetime.now(tz).isoformat()
    }).execute()


def get_history(user_id: int, limit: int = 20) -> list[dict]:
    """Oxirgi N ta xabarni qaytaradi (shifrdan chiqarilgan)."""
    res = supabase.table("messages") \
        .select("role, content") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .limit(limit) \
        .execute()

    messages = []
    for row in reversed(res.data):
        messages.append({
            "role": row["role"],
            "parts": [decrypt(row["content"])]
        })
    return messages


def clear_history(user_id: int):
    """Foydalanuvchi tarixini o'chiradi."""
    supabase.table("messages").delete().eq("user_id", user_id).execute()


# ──────────────────────────────────────────
#  XOTIRA (foydalanuvchi haqida ma'lumot)
# ──────────────────────────────────────────

def save_memory(user_id: int, key: str, value: str):
    """Foydalanuvchi haqida ma'lumot saqlaydi."""
    existing = supabase.table("memory") \
        .select("id") \
        .eq("user_id", user_id) \
        .eq("key", key) \
        .execute()

    if existing.data:
        supabase.table("memory").update({
            "value": encrypt(value),
            "updated_at": datetime.now(tz).isoformat()
        }).eq("user_id", user_id).eq("key", key).execute()
    else:
        supabase.table("memory").insert({
            "user_id": user_id,
            "key": key,
            "value": encrypt(value),
            "updated_at": datetime.now(tz).isoformat()
        }).execute()


def get_memory(user_id: int) -> dict:
    """Foydalanuvchi haqidagi barcha ma'lumotlarni qaytaradi."""
    res = supabase.table("memory") \
        .select("key, value") \
        .eq("user_id", user_id) \
        .execute()

    return {row["key"]: decrypt(row["value"]) for row in res.data}


# ──────────────────────────────────────────
#  ESLATMALAR
# ──────────────────────────────────────────

def save_reminder(user_id: int, text: str, remind_at: datetime, repeat: str = None):
    """Eslatma saqlaydi. repeat: None | 'daily' | 'weekly'"""
    supabase.table("reminders").insert({
        "user_id": user_id,
        "text": encrypt(text),
        "remind_at": remind_at.isoformat(),
        "repeat": repeat,
        "done": False
    }).execute()


def get_pending_reminders() -> list[dict]:
    """Vaqti kelgan va bajarilmagan eslatmalarni qaytaradi."""
    now = datetime.now(tz).isoformat()
    res = supabase.table("reminders") \
        .select("*") \
        .lte("remind_at", now) \
        .eq("done", False) \
        .execute()

    result = []
    for row in res.data:
        result.append({
            "id": row["id"],
            "user_id": row["user_id"],
            "text": decrypt(row["text"]),
            "repeat": row["repeat"],
            "remind_at": row["remind_at"]
        })
    return result


def mark_reminder_done(reminder_id: int, next_time: datetime = None):
    """Eslatmani bajarilgan deb belgilaydi yoki takroriy bo'lsa vaqtini yangilaydi."""
    if next_time:
        supabase.table("reminders").update({
            "remind_at": next_time.isoformat()
        }).eq("id", reminder_id).execute()
    else:
        supabase.table("reminders").update({
            "done": True
        }).eq("id", reminder_id).execute()
