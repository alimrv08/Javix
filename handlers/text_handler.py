from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_USER_ID
from services.gemini import ask_gemini
from services.reminder import parse_reminder_from_reply, parse_memory_from_reply, clean_reply
from database.supabase import save_reminder, save_memory


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text xabarlarni qayta ishlaydi."""
    user_id = update.effective_user.id
    
    # Faqat egasi ishlatishi mumkin
    if user_id != OWNER_USER_ID:
        await update.message.reply_text("⛔ Ruxsat yo'q.")
        return
    
    user_message = update.message.text
    
    # "Yozmoqda..." holati
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    
    # Gemini'dan javob olish
    reply = await ask_gemini(user_id, user_message)
    
    # Eslatma bormi?
    reminder = parse_reminder_from_reply(reply)
    if reminder:
        save_reminder(
            user_id=user_id,
            text=reminder["text"],
            remind_at=reminder["remind_at"],
            repeat=reminder["repeat"]
        )
    
    # Xotira bormi?
    memory = parse_memory_from_reply(reply)
    if memory:
        save_memory(user_id, memory["key"], memory["value"])
    
    # Teglarni tozalash
    clean = clean_reply(reply)
    
    # Javob yuborish
    if clean:
        await update.message.reply_text(clean)
    
    # Eslatma tasdiqi
    if reminder:
        await update.message.reply_text(
            f"✅ Eslatma saqlandi: *{reminder['text']}*\n"
            f"🕐 Vaqt: {reminder['remind_at'].strftime('%d.%m.%Y %H:%M')}",
            parse_mode="Markdown"
        )
