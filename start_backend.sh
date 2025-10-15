#!/bin/bash
cd /home/ubuntu/refactored_code
export $(grep -v '^#' .env | xargs)
export PYTHONPATH=/home/ubuntu/refactored_code:$PYTHONPATH
python3.11 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
