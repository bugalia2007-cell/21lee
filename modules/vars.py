import os

API_ID    = os.environ.get("API_ID", "")
API_HASH  = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# BUG FIX: WEBHOOK aur PORT pehle comment tha, main.py mein use ho raha tha → NameError aata tha
WEBHOOK = False  # Render/Heroku pe True karo
PORT = int(os.environ.get("PORT", 8080))
