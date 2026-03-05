#!/bin/bash
echo "==> Starting..."
export PYTHONPATH="/opt/render/project/src/modules:$PYTHONPATH"
gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 1 &
echo "==> Web server started"
python3 modules/main.py
