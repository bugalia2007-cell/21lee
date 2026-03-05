#!/bin/bash
echo "==> Starting Text Leech Bot..."

# Web server background mein (port ke liye zaruri)
gunicorn app:app --bind 0.0.0.0:${PORT:-8080} --workers 1 &

echo "==> Web server started on port ${PORT:-8080}"

# Bot start karo
python3 modules/main.py
