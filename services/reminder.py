import asyncio
import re
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
import pytz
from config import TIMEZONE
from database.supabase import save_reminder, get_pending_reminders, mark_reminder_done

tz = pytz.timezone(TIMEZONE)


def parse_reminder_from_reply(reply: str) -> dict | None:
    pattern = r'\[REMINDER:\s*(.+?)\s*\|\s*(.+?)\s*\|\s*repeat:(\w+)\]'
    match = re.search(pattern, reply, re.IGNORECASE)
    if not match:
        return None
    text = match.group(1).strip()
    date_str = match.group(2).strip()
    repeat = match.group(3).strip().lower()
    try:
        remind_at = parse_date(date_str)
        if remind_at.tzinfo is None:
            remind_at = tz.localize(remind_at)
        return {
            "text": text,
            "remind_at": remind_at,
            "repeat": None if repeat == "none" else repeat
        }
    except Exception:
        return None


def parse_memory_from_reply(reply: str) -> dict | None:
    pattern = r'\[MEMORY:\s*(.+?)\s*\|\s*(.+?)\]'
    match = re.search(pattern, reply, re.IGNORECASE)
    if not match:
        return None
    return {
        "key": match.group(1).strip(),
        "value": match.group(2).strip()
    }


def clean_reply(reply: str) -> str:
    reply = re.sub(r'\[REMINDER:[^\]]+\]', '', reply)
    reply = re.sub(r'\[MEMORY:[^\]]+\]', '', reply)
    reply = re.sub(r'\[SEARCH:[^\]]+\]', '', reply)
    return reply.strip()


async def reminder_loop(bot):
    while True:
        try:
            reminders = get_pending_reminders()
            for reminder in reminders:
                user_id = reminder["user_id"]
                text = reminder["text"]
                repeat = reminder["repeat"]
                reminder_id = reminder["id"]

                await bot.send_message(
                    chat_id=user_id,
                    text=f"⏰ *Eslatma:* {text}",
                    parse_mode="Markdown"
                )

                if repeat == "daily":
                    next_time = datetime.fromisoformat(reminder["remind_at"]) + timedelta(days=1)
                    mark_reminder_done(reminder_id, next_time)
                elif repeat == "weekly":
                    next_time = datetime.fromisoformat(reminder["remind_at"]) + timedelta(weeks=1)
                    mark_reminder_done(reminder_id, next_time)
                else:
                    mark_reminder_done(reminder_id)
        except Exception as e:
            print(f"Reminder loop xato: {e}")
        await asyncio.sleep(60)
