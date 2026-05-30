from gtts import gTTS
import tempfile
import os
import aiofiles


LANG_MAP = {
    "uz": "uz",
    "ru": "ru",
    "en": "en",
}


async def text_to_voice(text: str, lang: str = "uz") -> bytes:
    """
    Matnni ovozga aylantiradi.
    Qaytaradi: MP3 fayl bytes
    """
    tts_lang = LANG_MAP.get(lang, "uz")
    
    tts = gTTS(text=text, lang=tts_lang, slow=False)
    
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tts.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        async with aiofiles.open(tmp_path, "rb") as f:
            audio_bytes = await f.read()
        return audio_bytes
    finally:
        os.unlink(tmp_path)


def detect_response_lang(text: str) -> str:
    """
    Javob tilini aniqlaydi (oddiy usul).
    """
    cyrillic = sum(1 for c in text if '\u0400' <= c <= '\u04FF')
    latin = sum(1 for c in text if c.isalpha() and c.isascii())
    
    if cyrillic > latin:
        # O'zbek yoki Rus — keyingi tekshiruv
        uzbek_words = ["va", "bu", "men", "siz", "bilan", "uchun", "ham"]
        if any(w in text.lower() for w in uzbek_words):
            return "uz"
        return "ru"
    return "en"
