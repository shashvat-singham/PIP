@echo off
REM Setup script for Stock Research Platform (Windows)
echo ============================================================
echo   Stock Research Platform - Windows Setup
echo ============================================================
echo.

cd backend
python scripts\setup.py %*

echo.
echo Setup complete! To start the application, run:
echo   python scripts\start.py
echo.
pause

