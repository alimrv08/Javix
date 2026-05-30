from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_USER_ID, MAX_FILE_SIZE
from services.file_reader import process_document
from services.gemini import ask_gemini
from services.reminder import clean_reply


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fayl, rasm va hujjatlarni qayta ishlaydi."""
    user_id = update.effective_user.id
    
    if user_id != OWNER_USER_ID:
        await update.message.reply_text("⛔ Ruxsat yo'q.")
        return
    
    # Fayl turini aniqlash
    if update.message.document:
        doc = update.message.document
        file_id = doc.file_id
        filename = doc.file_name or "fayl"
        mime_type = doc.mime_type or ""
        file_size = doc.file_size or 0
    elif update.message.photo:
        photo = update.message.photo[-1]  # Eng yuqori sifat
        file_id = photo.file_id
        filename = "rasm.jpg"
        mime_type = "image/jpeg"
        file_size = photo.file_size or 0
    else:
        await update.message.reply_text("❌ Noma'lum fayl turi.")
        return
    
    # Fayl hajmi tekshirish
    if file_size > MAX_FILE_SIZE:
        await update.message.reply_text(
            f"❌ Fayl juda katta. Maksimum {MAX_FILE_SIZE // (1024*1024)}MB."
        )
        return
    
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="upload_document"
    )
    
    # Faylni yuklab olish
    file = await context.bot.get_file(file_id)
    file_bytes = await file.download_as_bytearray()
    
    await update.message.reply_text(f"📂 *{filename}* tahlil qilinmoqda...", parse_mode="Markdown")
    
    # Fayl tahlili
    analysis = await process_document(bytes(file_bytes), filename, mime_type)
    
    # Foydalanuvchi izoh qo'shgan bo'lsa
    caption = update.message.caption
    if caption:
        combined = f"Fayl tahlili:\n{analysis}\n\nFoydalanuvchi savoli: {caption}"
        reply = await ask_gemini(user_id, combined)
        clean = clean_reply(reply)
        await update.message.reply_text(clean or analysis)
    else:
        await update.message.reply_text(analysis)
