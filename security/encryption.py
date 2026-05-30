import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from config import ENCRYPTION_KEY


def _get_key() -> bytes:
    """ENCRYPTION_KEY dan 256-bit AES kaliti yasaydi."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"javix_salt_2024",
        iterations=100_000,
    )
    return kdf.derive(ENCRYPTION_KEY.encode())


def encrypt(text: str) -> str:
    """Matnni AES-256-GCM bilan shifrlaydi."""
    if not text:
        return ""
    key = _get_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, text.encode("utf-8"), None)
    result = base64.urlsafe_b64encode(nonce + ciphertext).decode()
    return result


def decrypt(token: str) -> str:
    """Shifrlangan matnni qaytaradi."""
    if not token:
        return ""
    try:
        key = _get_key()
        aesgcm = AESGCM(key)
        data = base64.urlsafe_b64decode(token.encode())
        nonce, ciphertext = data[:12], data[12:]
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode("utf-8")
    except Exception:
        return ""
