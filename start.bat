@echo off
REM Start script for Stock Research Platform (Windows)
echo ============================================================
echo   Stock Research Platform - Starting Application
echo ============================================================
echo.

cd backend
python scripts\start.py %*

