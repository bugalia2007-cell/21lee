from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "<h2>✅ Text Leech Bot is Running!</h2><p>Bot is alive and working.</p>", 200

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
