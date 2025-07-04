@echo off
title YesPlease Instagram Bot Setup

echo ========================================
echo YesPlease Instagram Bot Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Checking Python version...
python -c "import sys; print('Python version:', sys.version)"
echo.

REM Create virtual environment and install dependencies
echo Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo IMPORTANT: Before running the bot:
echo 1. Edit .env file with your Instagram credentials
echo 2. Add content files to the 'content' folder
echo 3. Test with a secondary account first
echo.
echo To run the bot:
echo - Run: python bot_manager.py (recommended)
echo - Or run: run_bot.bat
echo.
pause
