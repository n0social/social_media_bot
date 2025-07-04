@echo off
title YesPlease Social Media Bot (Instagram + X)

echo ========================================
echo YesPlease Social Media Bot
echo Instagram + X (Twitter) Automation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if .env is configured
findstr /C:"your_username_here\|your_x_api_key_here" .env >nul
if not errorlevel 1 (
    echo ERROR: Please configure your social media credentials in .env file
    echo Edit .env and replace placeholder values with your actual credentials
    pause
    exit /b 1
)

echo Starting Social Media Bot Manager...
echo.
call .venv\Scripts\activate.bat
python bot_manager.py

pause
