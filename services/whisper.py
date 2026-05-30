from services.gemini import transcribe_audio


async def voice_to_text(audio_bytes: bytes, file_ext: str = "ogg") -> tuple[str, str]:
    mime_type = f"audio/{file_ext}"
    return await transcribe_audio(audio_bytes, mime_type)
