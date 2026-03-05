from flask import Flask
import os
import threading
import time
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return "<h2>✅ Text Leech Bot is Running!</h2><p>Bot is alive and working.</p>", 200

@app.route("/health")
def health():
    return {"status": "ok"}, 200

def keep_alive():
    """Render free tier pe bot ko jaagne rakhne ke liye har 5 min ping karta hai"""
    time.sleep(30)  # startup ke baad wait karo
    url = os.environ.get("RENDER_EXTERNAL_URL", "https://two1lee.onrender.com")
    while True:
        try:
            requests.get(f"{url}/health", timeout=10)
            print("==> Keep-alive ping sent ✅")
        except Exception as e:
            print(f"==> Keep-alive ping failed: {e}")
        time.sleep(300)  # har 5 minute

# Keep-alive thread start karo
threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
