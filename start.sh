#!/bin/bash
echo "==> Starting..."
echo "==> Python: $(python3 --version)"

export PYTHONPATH="/opt/render/project/src/modules:$PYTHONPATH"

gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 1 &
echo "==> Web server started"

echo "==> ENV Check:"
echo "API_ID set: $([ -n "$API_ID" ] && echo YES || echo NO)"
echo "API_HASH set: $([ -n "$API_HASH" ] && echo YES || echo NO)"
echo "BOT_TOKEN set: $([ -n "$BOT_TOKEN" ] && echo YES || echo NO)"

echo "==> Starting bot now..."
python3 -u modules/main.py
EXIT_CODE=$?
echo "==> Bot exited with code: $EXIT_CODE"
