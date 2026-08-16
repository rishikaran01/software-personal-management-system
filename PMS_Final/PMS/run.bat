@echo off
echo ============================================
echo   Software Personal Management System
echo ============================================
echo.
echo Starting application...
python main.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Could not run. Make sure Python is installed.
    pause
)
