import asyncio
import logging
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from config import TELEGRAM_TOKEN, OWNER_USER_ID
from handlers.text_handler import handle_text
from handlers.voice_handler import handle_voice
from handlers.file_handler import handle_file
from services.reminder import reminder_loop
from database.supabase import clear_history

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────
#  BUYRUQLAR
# ──────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_USER_ID:
        await update.message.reply_text("⛔ Ruxsat yo'q.")
        return
    
    await update.message.reply_text(
        "👋 *Javix — Shaxsiy AI Yordamchingiz*\n\n"
        "Nima qila olaman:\n"
        "🗣 Text va ovozli xabarlar\n"
        "📄 PDF, Word hujjatlar tahlili\n"
        "🖼 Rasm tahlili\n"
        "⏰ Eslatmalar (bir martalik va takroriy)\n"
        "🧠 Sizni eslab qolaman\n"
        "🌐 Internet qidiruvi\n\n"
        "Shunchaki yozing yoki ovoz yuboring!",
        parse_mode="Markdown"
    )


async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_USER_ID:
        return
    clear_history(user_id)
    await update.message.reply_text("🗑 Suhbat tarixi tozalandi.")


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_USER_ID:
        return
    
    await update.message.reply_text(
        "*Buyruqlar:*\n"
        "/start — Boshlash\n"
        "/clear — Suhbat tarixini tozalash\n"
        "/help — Yordam\n\n"
        "*Eslatma misollari:*\n"
        "\"Ertaga soat 10da uchrashuv bor, eslatib qo'y\"\n"
        "\"Har kuni ertalab soat 8da sport qilishni eslatib tur\"\n\n"
        "*Fayl yuborish:*\n"
        "PDF, Word, rasm yuboring — tahlil qilaman\n"
        "Faylga izoh yozsangiz, savolingizga javob beraman",
        parse_mode="Markdown"
    )


# ──────────────────────────────────────────
#  ISHGA TUSHIRISH
# ──────────────────────────────────────────

async def post_init(app: Application):
    """Bot ishga tushganda bajariladigan amallar."""
    # Buyruqlar menyusi
    await app.bot.set_my_commands([
        BotCommand("start", "Boshlash"),
        BotCommand("clear", "Suhbat tarixini tozalash"),
        BotCommand("help", "Yordam"),
    ])
    
    # Eslatmalar loopini fon rejimda ishga tushirish
    asyncio.create_task(reminder_loop(app.bot))
    
    logger.info("✅ Javix bot ishga tushdi!")


def main():
    app = Application.builder() \
        .token(TELEGRAM_TOKEN) \
        .post_init(post_init) \
        .build()
    
    # Handlerlar
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("clear", cmd_clear))
    app.add_handler(CommandHandler("help", cmd_help))
    
    # Text xabarlar
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text
    ))
    
    # Ovoz xabarlar
    app.add_handler(MessageHandler(
        filters.VOICE | filters.AUDIO,
        handle_voice
    ))
    
    # Fayllar va rasmlar
    app.add_handler(MessageHandler(
        filters.Document.ALL | filters.PHOTO,
        handle_file
    ))
    
    logger.info("Bot polling rejimida ishlamoqda...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
