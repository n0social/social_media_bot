"""
Instagram Bot Configuration Validator and Health Checker
Validates all bot configurations and checks system health
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

class BotValidator:
    """Validates bot configuration and environment"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed_checks = []
        
    def add_error(self, message):
        self.errors.append(f"\u274c {message}")
        
    def add_warning(self, message):
        self.warnings.append(f"\u26a0\ufe0f  {message}")
        
    def add_success(self, message):
        self.passed_checks.append(f"\u2705 {message}")
        
    def validate_python_environment(self):
        """Validate Python environment"""
        # Python version
        if sys.version_info >= (3, 7):
            self.add_success(f"Python version {sys.version_info.major}.{sys.version_info.minor}")
        else:
            self.add_error(f"Python 3.7+ required (current: {sys.version_info.major}.{sys.version_info.minor})")
            
        # Required packages
        required_packages = [
            'instagrapi',
            'python-dotenv', 
            'schedule',
            'requests',
            'Pillow',
            'tweepy'
        ]
        
        for package in required_packages:
            try:
                if package == 'python-dotenv':
                    import dotenv
                elif package == 'Pillow':
                    import PIL
                else:
                    __import__(package)
                self.add_success(f"Package {package} installed")
            except ImportError:
                self.add_error(f"Package {package} not installed")
                
    def validate_environment_file(self):
        """Validate .env configuration file (credentials check removed for public release)"""
        env_file = Path('.env')
        
        if not env_file.exists():
            self.add_error(".env file not found")
            return
        # Credentials and placeholder checks removed for public release
        # Required variable checks removed for public release
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                
            # Check for required variables
            required_vars = [
                'INSTAGRAM_USERNAME',
                'INSTAGRAM_PASSWORD',
                'X_API_KEY',
                'X_API_SECRET', 
                'X_ACCESS_TOKEN',
                'MAX_LIKES_PER_HOUR',
                'MAX_COMMENTS_PER_HOUR',
                'MAX_FOLLOWS_PER_HOUR'
            ]
            
            for var in required_vars:
                if var in content:
                    self.add_success(f"Environment variable {var} present")
                else:
                    self.add_warning(f"Environment variable {var} missing (will use default)")
                    
        except Exception as e:
            self.add_error(f"Error reading .env file: {e}")
            
    def validate_content_folder(self):
        """Validate content folder and files"""
        content_folder = Path('content')
        
        if not content_folder.exists():
            self.add_error("Content folder not found")
            return
            
        # Check for content files
        supported_extensions = ['.jpg', '.jpeg', '.png', '.mp4']
        content_files = []
        
        for ext in supported_extensions:
            content_files.extend(content_folder.glob(f"*{ext}"))
            
        if not content_files:
            self.add_warning("No content files found - add images/videos to content folder")
        else:
            self.add_success(f"Found {len(content_files)} content files")
            
            # Check file sizes
            large_files = []
            for file in content_files:
                size_mb = file.stat().st_size / (1024 * 1024)
                if size_mb > 50:  # 50MB limit
                    large_files.append(f"{file.name} ({size_mb:.1f}MB)")
                    
            if large_files:
                self.add_warning(f"Large files detected (may fail to upload): {', '.join(large_files)}")
                
    def validate_permissions(self):
        """Validate file and folder permissions"""
        # Check write permissions for required directories
        required_dirs = ['logs', 'data']
        
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            try:
                dir_path.mkdir(exist_ok=True)
                # Test write permission
                test_file = dir_path / 'test_write.tmp'
                test_file.write_text('test')
                test_file.unlink()
                self.add_success(f"Write permission for {dir_name}/ folder")
            except Exception as e:
                self.add_error(f"No write permission for {dir_name}/ folder: {e}")
                
    def validate_network_connectivity(self):
        """Validate network connectivity"""
        try:
            import requests
            
            # Test basic internet connectivity
            response = requests.get('https://httpbin.org/status/200', timeout=10)
            if response.status_code == 200:
                self.add_success("Internet connectivity available")
            else:
                self.add_warning("Internet connectivity issues detected")
                
            # Test Instagram accessibility (basic check)
            try:
                response = requests.head('https://www.instagram.com', timeout=10)
                if response.status_code == 200:
                    self.add_success("Instagram.com accessible")
                else:
                    self.add_warning("Instagram.com may not be accessible")
            except:
                self.add_warning("Cannot reach Instagram.com (may be blocked)")
                
        except ImportError:
            self.add_warning("Cannot test network connectivity - requests library not available")
        except Exception as e:
            self.add_warning(f"Network connectivity test failed: {e}")
            
    def validate_security_settings(self):
        """Validate security and safety settings"""
        try:
            from bot_config import BotConfig
            
            # Check rate limits are reasonable
            if BotConfig.RATE_LIMITS['likes_per_hour'] > 50:
                self.add_warning("Like rate limit is high - consider reducing to avoid detection")
            else:
                self.add_success("Like rate limit is conservative")
                
            if BotConfig.RATE_LIMITS['follows_per_hour'] > 30:
                self.add_warning("Follow rate limit is high - consider reducing")
            else:
                self.add_success("Follow rate limit is conservative")
                
            # Check delays
            if BotConfig.DELAYS['min_action_delay'] < 30:
                self.add_warning("Minimum action delay is very short - consider increasing")
            else:
                self.add_success("Action delays are reasonable")
                
        except ImportError:
            self.add_warning("Cannot validate bot configuration - bot_config.py not available")
            
    def check_existing_data(self):
        """Check for existing bot data and logs"""
        # Check for existing session
        session_file = Path('data/session.json')
        if session_file.exists():
            self.add_success("Existing Instagram session found")
        else:
            self.add_success("No existing session (will create on first login)")
            
        # Check for activity logs
        activity_file = Path('data/activity_tracker.json')
        if activity_file.exists():
            try:
                with open(activity_file, 'r') as f:
                    data = json.load(f)
                self.add_success("Activity tracking data found")
            except:
                self.add_warning("Activity tracking data corrupted")
        else:
            self.add_success("No existing activity data (will create on first run)")
            
        # Check log files
        log_files = list(Path('logs').glob('*.log')) if Path('logs').exists() else []
        if log_files:
            self.add_success(f"Found {len(log_files)} existing log files")
        else:
            self.add_success("No existing logs (will create on first run)")
            
    def run_full_validation(self):
        """Run complete validation suite"""
        print("🔍 Instagram Bot Validation Report")
        print("=" * 50)
        print(f"Validation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all validations
        validation_steps = [
            ("Python Environment", self.validate_python_environment),
            ("Environment Configuration", self.validate_environment_file),
            ("Content Folder", self.validate_content_folder),
            ("File Permissions", self.validate_permissions),
            ("Network Connectivity", self.validate_network_connectivity),
            ("Security Settings", self.validate_security_settings),
            ("Existing Data", self.check_existing_data)
        ]
        
        for step_name, step_func in validation_steps:
            print(f"Checking {step_name}...")
            try:
                step_func()
            except Exception as e:
                self.add_error(f"Validation step '{step_name}' failed: {e}")
            print()
            
        # Print results
        if self.passed_checks:
            print("✅ PASSED CHECKS:")
            for check in self.passed_checks:
                print(f"   {check}")
            print()
            
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"   {warning}")
            print()
            
        if self.errors:
            print("❌ ERRORS (Must Fix):")
            for error in self.errors:
                print(f"   {error}")
            print()
            
        # Summary
        total_checks = len(self.passed_checks) + len(self.warnings) + len(self.errors)
        print("📊 SUMMARY:")
        print(f"   Total checks: {total_checks}")
        print(f"   Passed: {len(self.passed_checks)}")
        print(f"   Warnings: {len(self.warnings)}")
        print(f"   Errors: {len(self.errors)}")
        print()
        
        if self.errors:
            print("❌ Bot is NOT ready to run. Please fix errors above.")
            return False
        elif self.warnings:
            print("⚠️  Bot can run but has warnings. Review warnings above.")
            return True
        else:
            print("✅ Bot is ready to run! All checks passed.")
            return True

def main():
    """Main validation function"""
    validator = BotValidator()
    is_ready = validator.run_full_validation()
    
    if is_ready:
        print("🚀 Next step: Run 'python bot_manager.py' to start the bot")
    else:
        print("🔧 Fix the errors above and run validation again")
        
    return is_ready

if __name__ == "__main__":
    main()
