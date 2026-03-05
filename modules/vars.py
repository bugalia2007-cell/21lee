import os
from dotenv import load_dotenv

load_dotenv()

API_ID    = int(os.environ.get("API_ID", 0))
API_HASH  = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBHOOK   = os.environ.get("WEBHOOK", "False").lower() == "true"
PORT      = int(os.environ.get("PORT", 10000))

missing = []
if not API_ID:    missing.append("API_ID")
if not API_HASH:  missing.append("API_HASH")
if not BOT_TOKEN: missing.append("BOT_TOKEN")

if missing:
    raise ValueError(
        f"\n❌ Yeh variables set nahi hain:\n" +
        "\n".join(f"  • {v}" for v in missing) +
        "\n\n📌 Render Dashboard → Environment Variables mein add karo!\n"
    )
