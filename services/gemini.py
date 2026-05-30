import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, CONTEXT_MESSAGES
from database.supabase import get_history, get_memory, save_message

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """Sen Javix — shaxsiy AI yordamchisan.
Foydalanuvchining sodiq yordamchisi, do'sti va maslahatchi sifatida ish ko'rasan.

Qoidalar:
1. Foydalanuvchi qaysi tilda yozsa, o'sha tilda javob ber (o'zbek/rus/ingliz)
2. Qisqa, aniq va foydali javob ber — keraksiz so'z ishlatma
3. Foydalanuvchi haqidagi ma'lumotlarni esda saqlaysan
4. Agar bilmasang — "bilmayman" de, to'qima
5. Doim xushmuomala va ijobiy bo'l

Qo'shimcha ko'rsatmalar:
- Eslatma so'ralsa: [REMINDER: matn | YYYY-MM-DD HH:MM | repeat:none/daily/weekly] formatida yoz
- Muhim ma'lumot eslab qolinsa: [MEMORY: kalit | qiymat] formatida yoz
"""


def build_context(user_id: int) -> str:
    memory = get_memory(user_id)
    if not memory:
        return ""
    lines = ["Foydalanuvchi haqida ma'lumot:"]
    for key, val in memory.items():
        lines.append(f"- {key}: {val}")
    return "\n".join(lines)


async def ask_gemini(user_id: int, user_message: str) -> str:
    save_message(user_id, "user", user_message)

    history = get_history(user_id, CONTEXT_MESSAGES)
    memory_context = build_context(user_id)

    full_system = SYSTEM_PROMPT
    if memory_context:
        full_system += f"\n\n{memory_context}"

    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=full_system
    )

    chat_history = history[:-1] if history else []
    chat = model.start_chat(history=chat_history)
    response = chat.send_message(user_message)
    reply = response.text

    save_message(user_id, "model", reply)
    return reply


async def analyze_image(image_bytes: bytes, prompt: str = "Bu rasmda nima bor?") -> str:
    model = genai.GenerativeModel(GEMINI_MODEL)
    image_part = {"mime_type": "image/jpeg", "data": image_bytes}
    response = model.generate_content([prompt, image_part])
    return response.text


async def analyze_document(content: str, filename: str) -> str:
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=SYSTEM_PROMPT
    )
    prompt = f"Fayl nomi: {filename}\n\nMazmun:\n{content}\n\nShu hujjatni qisqacha tahlil qil."
    response = model.generate_content(prompt)
    return response.text


async def transcribe_audio(audio_bytes: bytes, mime_type: str = "audio/ogg") -> tuple[str, str]:
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    response = model.generate_content([
        {"inline_data": {"mime_type": mime_type, "data": audio_bytes}},
        "Bu audio fayldagi nutqni aynan transkripsiya qil. Faqat aytilgan so'zlarni yoz, boshqa hech narsa qo'shma."
    ])
    
    text = response.text.strip()
    
    # Tilni aniqlash
    cyrillic = sum(1 for c in text if '\u0400' <= c <= '\u04FF')
    latin = sum(1 for c in text if c.isalpha() and c.isascii())
    if cyrillic > latin:
        uzbek_words = ["va", "bu", "men", "siz", "bilan", "uchun", "ham", "yo'q", "ha"]
        lang = "uz" if any(w in text.lower() for w in uzbek_words) else "ru"
    else:
        lang = "en"
    
    return text, lang
