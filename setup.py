#!/usr/bin/env python3
"""
Instagram Bot Setup Script
Helps set up and configure the Instagram bot for first-time users
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def setup_environment():
    """Set up environment variables"""
    print("\n🔧 Setting up environment configuration...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env file already exists. Checking configuration...")
        
        with open(env_file, 'r') as f:
            content = f.read()
            
        if "your_username_here" in content:
            print("❌ Please edit .env file with your Instagram credentials")
            return False
        else:
            print("✅ Environment configuration looks good!")
            return True
    else:
        print("❌ .env file not found. Please create it from the template.")
        return False

def check_content_folder():
    """Check if content folder exists and has files"""
    print("\n📁 Checking content folder...")
    
    content_folder = Path("content")
    if not content_folder.exists():
        print("❌ Content folder not found")
        return False
        
    # Check for content files
    content_files = []
    for ext in ['.jpg', '.jpeg', '.png', '.mp4']:
        content_files.extend(content_folder.glob(f"*{ext}"))
        
    if not content_files:
        print("⚠️  No content files found in content folder")
        print("Please add some images or videos to post")
        return False
    else:
        print(f"✅ Found {len(content_files)} content files")
        return True

def test_imports():
    """Test if all required packages can be imported"""
    print("\n🔍 Testing package imports...")
    
    required_packages = [
        'instagrapi',
        'dotenv',
        'schedule',
        'requests',
        'PIL'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            failed_imports.append(package)
            
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All packages imported successfully!")
        return True

def main():
    """Main setup function"""
    print("🚀 YesPlease Instagram Bot Setup")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", install_dependencies),
        ("Environment Config", setup_environment),
        ("Content Folder", check_content_folder),
        ("Package Imports", test_imports)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        if not check_func():
            all_passed = False
            
    print("\n" + "=" * 40)
    
    if all_passed:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Add your content files to the 'content/' folder")
        print("2. Edit .env with your Instagram credentials")
        print("3. Run: python bot_manager.py")
        print("\n⚠️  Important: Test with a secondary account first!")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        
    return all_passed

if __name__ == "__main__":
    main()
