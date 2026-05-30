import aiofiles
import PyPDF2
import docx
import io
from services.gemini import analyze_image, analyze_document


async def read_pdf(file_bytes: bytes) -> str:
    """PDF fayldan matn ajratadi."""
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


async def read_word(file_bytes: bytes) -> str:
    """Word fayldan matn ajratadi."""
    doc = docx.Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text.strip()


async def process_document(file_bytes: bytes, filename: str, mime_type: str) -> str:
    """Hujjat turini aniqlab, tahlil qiladi."""
    
    if mime_type == "application/pdf" or filename.endswith(".pdf"):
        text = await read_pdf(file_bytes)
        if not text:
            return "❌ PDF fayldan matn ajratib bo'lmadi (skanerlangan bo'lishi mumkin)."
        return await analyze_document(text, filename)
    
    elif mime_type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword"
    ] or filename.endswith((".docx", ".doc")):
        text = await read_word(file_bytes)
        if not text:
            return "❌ Word fayldan matn ajratib bo'lmadi."
        return await analyze_document(text, filename)
    
    elif mime_type.startswith("image/"):
        return await analyze_image(file_bytes, "Bu rasmni batafsil tahlil qil.")
    
    else:
        return f"❌ '{filename}' fayl turi hozircha qo'llab-quvvatlanmaydi.\nQo'llab-quvvatlanadigan: PDF, Word, Rasm"
