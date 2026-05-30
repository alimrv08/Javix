from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_USER_ID, MAX_VOICE_DURATION
from services.whisper import voice_to_text
from services.gemini import ask_gemini
from services.tts import text_to_voice, detect_response_lang
from services.reminder import parse_reminder_from_reply, parse_memory_from_reply, clean_reply
from database.supabase import save_reminder, save_memory
import io


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != OWNER_USER_ID:
        await update.message.reply_text("⛔ Ruxsat yo'q.")
        return

    voice = update.message.voice or update.message.audio

    if voice.duration > MAX_VOICE_DURATION:
        await update.message.reply_text(f"❌ Maksimum {MAX_VOICE_DURATION // 60} daqiqa.")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Ovozni yuklab olish
    file = await context.bot.get_file(voice.file_id)
    file_bytes = await file.download_as_bytearray()

    # Gemini orqali ovoz → text
    text, detected_lang = await voice_to_text(bytes(file_bytes), "ogg")

    if not text:
        await update.message.reply_text("❌ Ovozni tushunib bo'lmadi.")
        return

    # Transkripsiyani ko'rsatish
    await update.message.reply_text(f"🎤 *Siz:* {text}", parse_mode="Markdown")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Gemini javob
    reply = await ask_gemini(user_id, text)

    reminder = parse_reminder_from_reply(reply)
    if reminder:
        save_reminder(user_id, reminder["text"], reminder["remind_at"], reminder["repeat"])

    memory = parse_memory_from_reply(reply)
    if memory:
        save_memory(user_id, memory["key"], memory["value"])

    clean = clean_reply(reply)

    if not clean:
        return

    # Text javob yuborish
    await update.message.reply_text(clean)

    # Ovoz javob
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="record_voice")
        response_lang = detect_response_lang(clean)
        audio_bytes = await text_to_voice(clean, response_lang)
        await update.message.reply_voice(voice=io.BytesIO(audio_bytes))
    except Exception as e:
        print(f"TTS xato: {e}")

    if reminder:
        await update.message.reply_text(
            f"✅ Eslatma: *{reminder['text']}*\n🕐 {reminder['remind_at'].strftime('%d.%m.%Y %H:%M')}",
            parse_mode="Markdown"
        )
