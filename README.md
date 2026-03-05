<div align="center">

# 📥 Text Leech Bot

**Telegram bot jo .txt file se links download karke Telegram pe upload karta hai**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0-green?style=for-the-badge)](https://pyrogram.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

</div>

---

## ✨ Features

- 📁 `.txt` file se bulk links download karta hai
- 🎬 Videos download & upload (YouTube, VisionIAS, ClassPlus, m3u8, etc.)
- 📄 PDFs download & upload
- ☁️ Google Drive support
- 🖼️ Custom thumbnail support
- 📊 Upload progress bar
- 🎯 Quality select: 144p, 240p, 360p, 480p, 720p, 1080p

---

## ⚙️ Setup

### 1. Clone karo
```bash
git clone https://github.com/YOUR_USERNAME/text-leech-bot.git
cd text-leech-bot
```

### 2. Requirements install karo
```bash
pip install -r requirements.txt
```

### 3. Environment variables set karo
```bash
cp .env.example .env
# Ab .env file mein apni values bharo
```

### 4. Bot chalao
```bash
python3 modules/main.py
```

---

## 🔑 Required Variables

| Variable | Description | Kahan se milega |
|----------|-------------|-----------------|
| `API_ID` | Telegram API ID | [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API Hash | [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Bot Token | [@BotFather](https://t.me/BotFather) |
| `PORT` | Web server port (default: 8080) | Optional |

---

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Bot alive check |
| `/upload` | .txt file se links upload karo |
| `/stop` | Bot restart karo |

---

## 📝 TXT File Format

Har line mein ek link hona chahiye, is format mein:
```
Video Name 1://https://youtube.com/watch?v=xxxxx
Video Name 2://https://youtu.be/xxxxx
PDF Name://https://example.com/file.pdf
```

---

## 🚀 Deploy

### Heroku
[![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Docker
```bash
docker build -t text-leech-bot .
docker run -e API_ID=xxx -e API_HASH=xxx -e BOT_TOKEN=xxx text-leech-bot
```

---

## 📦 Dependencies

- [Pyrogram](https://pyrogram.org/) — Telegram MTProto client
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — Video downloader
- [aria2c](https://aria2.github.io/) — Fast download manager
- [FFmpeg](https://ffmpeg.org/) — Video processing

---

## ⚠️ Disclaimer

Yeh bot sirf educational purposes ke liye hai. Kisi bhi copyrighted content ko download karna illegal ho sakta hai. Bot ka istemal apni zimmedari par karein.

---

<div align="center">

**Made with ❤️ | Bug fixes & improvements included**

</div>
