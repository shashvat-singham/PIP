#!/bin/bash
# Setup script for Stock Research Platform (Linux/macOS)

echo "============================================================"
echo "  Stock Research Platform - Setup"
echo "============================================================"
echo ""

cd backend
python3 scripts/setup.py "$@"

echo ""
echo "Setup complete! To start the application, run:"
echo "  ./start.sh"
echo ""

