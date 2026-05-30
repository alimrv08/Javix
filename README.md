# 🤖 Javix — Shaxsiy AI Yordamchi

Telegram orqali ishlaydigan shaxsiy AI yordamchi.

---

## 📁 Papka tuzilmasi

```
javix/
├── bot.py                    # Asosiy fayl
├── config.py                 # Sozlamalar
├── requirements.txt          # Kutubxonalar
├── Dockerfile                # Railway uchun
├── .env                      # API kalitlar (SIZ TO'LDIRASIZ)
├── handlers/
│   ├── text_handler.py       # Text xabarlar
│   ├── voice_handler.py      # Ovoz xabarlar
│   └── file_handler.py       # Fayllar
├── services/
│   ├── gemini.py             # AI xizmati
│   ├── whisper.py            # Ovoz → Text
│   ├── tts.py                # Text → Ovoz
│   ├── file_reader.py        # Fayl tahlili
│   └── reminder.py           # Eslatmalar
├── database/
│   ├── supabase.py           # Ma'lumotlar bazasi
│   └── schema.sql            # Jadvallar (bir marta ishga tushiring)
└── security/
    └── encryption.py         # AES-256 shifrlash
```

---

## ⚙️ O'rnatish

### 1-qadam — .env faylni to'ldiring

`.env` faylini oching va har bir qatorni to'ldiring:

```
TELEGRAM_TOKEN=BotFather'dan olgan tokeningiz
GEMINI_API_KEY=Google AI Studio'dan olgan kalit
SUPABASE_URL=https://sizning-id.supabase.co
SUPABASE_ANON_KEY=Supabase'dan anon kalit
SUPABASE_SERVICE_KEY=Supabase'dan service_role kalit
ENCRYPTION_KEY=ixtiyoriy_32_belgili_maxfiy_so'z_yozing
OWNER_USER_ID=Telegram user ID (quyida qanday olishni ko'ring)
```

**Telegram User ID olish:**
1. Telegram'da @userinfobot ga boring
2. /start yuboring
3. Raqamni (ID) nusxalab .env ga yozing

### 2-qadam — Supabase jadvallarini yarating

1. supabase.com ga kiring
2. Loyihangizni oching
3. SQL Editor → New query
4. `database/schema.sql` faylining mazmunini ko'chiring
5. Run tugmasini bosing

### 3-qadam — Railway'ga deploy qiling

**Variant A — GitHub orqali (tavsiya):**
1. Bu papkani GitHub'ga yuklang
2. railway.app → New Project → GitHub repo tanlang
3. Variables bo'limiga .env dagi barcha kalitlarni kiriting
4. Deploy tugmasini bosing

**Variant B — Railway CLI:**
```bash
npm install -g @railway/cli
railway login
railway up
```

### 4-qadam — Test qiling

Telegram'da botingizga /start yuboring!

---

## 💬 Foydalanish

### Asosiy buyruqlar:
- `/start` — Boshlash
- `/clear` — Suhbat tarixini tozalash
- `/help` — Yordam

### Nima qila oladi:
- **Text va ovoz** — Yozing yoki ovoz yuboring
- **PDF/Word** — Hujjat yuboring, tahlil qiladi
- **Rasm** — Rasm yuboring, tavsiflab beradi
- **Eslatma** — "Ertaga soat 10da uchrashuv bor, eslatib qo'y"
- **Takroriy eslatma** — "Har kuni ertalab soat 8da yugurish eslatib tur"

---

## 🔐 Xavfsizlik

- Barcha ma'lumotlar AES-256-GCM bilan shifrlangan
- Faqat siz (OWNER_USER_ID) bot bilan muloqot qila olasiz
- API kalitlar faqat .env faylda, kodda yo'q

---

## 💰 Xarajat

| Xizmat | Narx |
|--------|------|
| Telegram Bot | Bepul |
| Gemini 1.5 Flash | Bepul (1500 req/kun) |
| Whisper (local) | Bepul |
| Google TTS | Bepul (1M belgi/oy) |
| Supabase | Bepul (500MB) |
| Railway | $5/oy |
| **Jami** | **$5/oy** |

---

## ❓ Muammo bo'lsa

Railway'da **Logs** bo'limini tekshiring — xatolar u yerda ko'rinadi.
