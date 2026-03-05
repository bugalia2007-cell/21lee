#!/bin/bash
echo "==> Starting Text Leech Bot..."
echo "==> Python: $(python3 --version)"

# Modules folder ko Python path mein add karo
export PYTHONPATH="/opt/render/project/src/modules:$PYTHONPATH"

# Session folder
mkdir -p /tmp/bot

# ENV check
echo "==> ENV Check:"
echo "API_ID set:    $([ -n "$API_ID" ]    && echo YES || echo NO)"
echo "API_HASH set:  $([ -n "$API_HASH" ]  && echo YES || echo NO)"
echo "BOT_TOKEN set: $([ -n "$BOT_TOKEN" ] && echo YES || echo NO)"

# Web server background mein (port ke liye)
gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 1 &
echo "==> Web server started on port ${PORT:-10000}"

# Bot start karo
echo "==> Starting bot now..."
python3 -u modules/main.py 2>&1
echo "==> Bot exited with code: $?"
