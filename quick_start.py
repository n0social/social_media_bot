"""
Quick Start Guide for YesPlease Instagram Bot
"""

import os
import sys
from pathlib import Path

def print_header():
    print("🚀 YesPlease Instagram Bot - Quick Start Guide")
    print("=" * 50)
    print()

def check_setup():
    print("📋 Setup Checklist:")
    print("-" * 20)
    
    checks = []
    
    # Check Python version
    if sys.version_info >= (3, 7):
        checks.append(("✅", "Python 3.7+ installed"))
    else:
        checks.append(("❌", f"Python 3.7+ required (current: {sys.version})"))
    
    # Check .env file
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
        if 'your_username_here' not in content:
            checks.append(("✅", ".env file configured"))
        else:
            checks.append(("❌", ".env file needs Instagram credentials"))
    else:
        checks.append(("❌", ".env file missing"))
    
    # Check content folder
    content_folder = Path('content')
    if content_folder.exists():
        content_files = list(content_folder.glob('*.jpg')) + list(content_folder.glob('*.png')) + list(content_folder.glob('*.mp4'))
        if content_files:
            checks.append(("✅", f"Content folder has {len(content_files)} files"))
        else:
            checks.append(("⚠️", "Content folder empty - add images/videos"))
    else:
        checks.append(("❌", "Content folder missing"))
    
    # Check dependencies
    try:
        import instagrapi
        checks.append(("✅", "Instagram API library installed"))
    except ImportError:
        checks.append(("❌", "Dependencies not installed"))
    
    for status, message in checks:
        print(f"{status} {message}")
    
    print()
    return all(check[0] == "✅" for check in checks if check[0] in ["✅", "❌"])

def show_next_steps(setup_complete):
    print("🎯 Next Steps:")
    print("-" * 15)
    
    if not setup_complete:
        print("1. Run setup: python setup.py")
        print("2. Edit .env file with your Instagram credentials")
        print("3. Add content files to content/ folder")
        print("4. Install dependencies: pip install -r requirements.txt")
    else:
        print("✅ Setup complete! Ready to run the bot.")
        print()
        print("🎮 Running Options:")
        print("1. Interactive mode: python bot_manager.py")
        print("2. Windows batch file: run_bot.bat")
        print("3. Direct execution: python instagram_bot.py")
    
    print()

def show_safety_reminders():
    print("⚠️  Safety Reminders:")
    print("-" * 20)
    print("• Start with a secondary/test account")
    print("• Use conservative limits initially")
    print("• Monitor for any Instagram warnings")
    print("• Don't run 24/7 - take breaks")
    print("• Respect Instagram's Terms of Service")
    print("• This tool is for educational purposes")
    print()

def show_project_structure():
    print("📁 Project Structure:")
    print("-" * 20)
    print("instagram_bot.py      - Main bot script")
    print("bot_manager.py        - Interactive management")
    print("advanced_bot.py       - Enhanced version with safety features")
    print("bot_config.py         - Configuration and safety settings")
    print(".env                  - Your credentials (keep private!)")
    print("content/              - Your images/videos to post")
    print("logs/                 - Bot activity logs")
    print("data/                 - Bot data and session files")
    print("requirements.txt      - Python dependencies")
    print("setup.py              - Setup script")
    print("setup.bat             - Windows setup script")
    print("run_bot.bat           - Windows run script")
    print()

def main():
    print_header()
    setup_complete = check_setup()
    show_next_steps(setup_complete)
    show_safety_reminders()
    show_project_structure()
    
    print("📚 For detailed information, see README.md")
    print("🆘 For issues, check the logs/ folder")
    print()
    print("Happy botting! 🤖✨")

if __name__ == "__main__":
    main()
