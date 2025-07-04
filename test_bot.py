#!/usr/bin/env python3
"""
Instagram Bot Test Script
Quick test to verify all components are working
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required imports work"""
    print("🧪 Testing Python imports...")
    
    try:
        import instagrapi
        print("✅ instagrapi imported successfully")
    except ImportError as e:
        print(f"❌ instagrapi import failed: {e}")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        import schedule
        print("✅ schedule imported successfully")
    except ImportError as e:
        print(f"❌ schedule import failed: {e}")
        return False
    
    try:
        import requests
        print(f"✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        import PIL
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    return True

def test_bot_modules():
    """Test that our bot modules can be imported"""
    print("\n🤖 Testing bot modules...")
    
    try:
        from bot_config import BotConfig, SafetyChecker
        print("✅ bot_config imported successfully")
        
        # Test configuration
        print(f"   - Max likes per hour: {BotConfig.RATE_LIMITS['likes_per_hour']}")
        print(f"   - Max comments per hour: {BotConfig.RATE_LIMITS['comments_per_hour']}")
        print(f"   - Safety delays: {BotConfig.DELAYS['min_action_delay']}-{BotConfig.DELAYS['max_action_delay']}s")
        
    except ImportError as e:
        print(f"❌ bot_config import failed: {e}")
        return False
    
    try:
        from instagram_bot import InstagramBot
        print("✅ instagram_bot imported successfully")
    except ImportError as e:
        print(f"❌ instagram_bot import failed: {e}")
        return False
    
    try:
        from advanced_bot import AdvancedInstagramBot
        print("✅ advanced_bot imported successfully")
    except ImportError as e:
        print(f"❌ advanced_bot import failed: {e}")
        return False
    
    return True

def test_environment_setup():
    """Test environment setup"""
    print("\n⚙️  Testing environment setup...")
    
    # Check .env file
    if os.path.exists('.env'):
        print("✅ .env file exists")
        with open('.env', 'r') as f:
            content = f.read()
        
        if 'INSTAGRAM_USERNAME' in content:
            print("✅ INSTAGRAM_USERNAME variable present")
        else:
            print("❌ INSTAGRAM_USERNAME variable missing")
            
        if 'your_username_here' in content:
            print("⚠️  Please configure your Instagram credentials in .env")
        else:
            print("✅ Instagram credentials appear to be configured")
    else:
        print("❌ .env file not found")
        return False
    
    # Check content folder
    content_path = Path('content')
    if content_path.exists():
        print("✅ content folder exists")
        content_files = list(content_path.glob('*.jpg')) + list(content_path.glob('*.png')) + list(content_path.glob('*.mp4'))
        if content_files:
            print(f"✅ Found {len(content_files)} content files")
        else:
            print("⚠️  No content files found - add images/videos to content folder")
    else:
        print("❌ content folder not found")
        return False
    
    return True

def test_bot_initialization():
    """Test bot initialization (without login)"""
    print("\n🚀 Testing bot initialization...")
    
    try:
        from instagram_bot import InstagramBot
        bot = InstagramBot()
        print("✅ Basic bot initialized successfully")
        
        # Test activity log
        activity = bot.activity_log
        print(f"✅ Activity tracking initialized: {len(activity)} fields")
        
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
        return False
    
    try:
        from advanced_bot import AdvancedInstagramBot
        advanced_bot = AdvancedInstagramBot()
        print("✅ Advanced bot initialized successfully")
        
        # Test activity summary
        summary = advanced_bot.get_activity_summary()
        print(f"✅ Activity summary generated: {summary}")
        
    except Exception as e:
        print(f"❌ Advanced bot initialization failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Instagram Bot Test Suite")
    print("=" * 40)
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
    tests = [
        ("Python Imports", test_imports),
        ("Bot Modules", test_bot_modules),
        ("Environment Setup", test_environment_setup),
        ("Bot Initialization", test_bot_initialization)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
        print()
    
    print("=" * 40)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready to use.")
        print("\n📋 Next steps:")
        print("1. Configure Instagram credentials in .env")
        print("2. Add content files to content/ folder")
        print("3. Run: python bot_manager.py")
    else:
        print("🔧 Some tests failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
