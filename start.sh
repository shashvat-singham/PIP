#!/bin/bash
# Start script for Stock Research Platform (Linux/macOS)

echo "============================================================"
echo "  Stock Research Platform - Starting Application"
echo "============================================================"
echo ""

cd backend
python3 scripts/start.py "$@"

