#!/usr/bin/env bash
set -e

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

PORT="${APP_PORT:-8000}"
uvicorn app.main:app --reload --host 0.0.0.0 --port "$PORT"
