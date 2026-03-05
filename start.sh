#!/bin/bash
echo "==> Starting..."
echo "==> Python: $(python3 --version)"

export PYTHONPATH="/opt/render/project/src/modules:$PYTHONPATH"

gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 1 &
echo "==> Web server started"

echo "==> Starting bot now..."
python3 -u modules/main.py 2>&1
echo "==> Bot exited!"
