import os
import time
import random
import schedule
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import json

# Import our platform-specific bots
from instagram_bot import InstagramBot
# from x_bot import XBot  # Disabled for public release

class UnifiedSocialMediaBot:
    """Unified bot that manages both Instagram and X (credentials removed)"""
    
    def __init__(self):
        load_dotenv()
        self.setup_logging()
        
        # Initialize platform bots
        self.instagram_bot = None
        # self.twitter_bot = None  # Disabled for public release
        # self.x_bot = None  # Disabled for public release
        
        # Platform settings
        self.enable_instagram = os.getenv('ENABLE_INSTAGRAM', 'true').lower() == 'true'
        # self.enable_twitter = os.getenv('ENABLE_TWITTER', 'true').lower() == 'true'  # Disabled
        # self.enable_x = os.getenv('ENABLE_X', 'true').lower() == 'true'  # Disabled
        
        self.initialize_bots()
        
    def setup_logging(self):
        """Setup logging for unified bot"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/unified_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('UnifiedBot')
        
    def initialize_bots(self):
        """Initialize platform-specific bots (X bot disabled for public release)"""
        # Initialize Instagram bot
        if self.enable_instagram:
            try:
                self.instagram_bot = InstagramBot()
                self.logger.info("Instagram bot initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize Instagram bot: {e}")
                self.instagram_bot = None
        # X bot initialization removed

    def run_instagram_activities(self):
        """Run Instagram activities"""
        if self.instagram_bot:
            try:
                self.logger.info("Running Instagram activities")
                self.instagram_bot.run_daily_activities()
            except Exception as e:
                self.logger.error(f"Error running Instagram activities: {e}")
        else:
            self.logger.info("Instagram bot not available")
            
    # Twitter and X activities removed
    
    def run_all_activities(self):
        """Run activities on all platforms"""
        self.logger.info("Starting unified social media bot activities")
        
        # Add delay between platforms
        if self.instagram_bot:
            self.run_instagram_activities()
            time.sleep(random.randint(300, 600))  # 5-10 minute delay
            
        # Twitter and X activities removed
            
        self.logger.info("Completed unified social media bot activities")
        
    def get_activity_summary(self):
        """Get activity summary from all platforms"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'platforms': {}
        }
        
        if self.instagram_bot:
            try:
                summary['platforms']['instagram'] = self.instagram_bot.get_activity_summary()
            except:
                summary['platforms']['instagram'] = {'error': 'Failed to get Instagram summary'}
                
        # Twitter and X summary removed
                
        return summary
        
    def start_scheduler(self):
        """Start the unified bot scheduler"""
        self.logger.info("Starting unified social media bot scheduler")
        
        # Schedule activities throughout the day
        schedule.every().day.at("09:00").do(self.run_all_activities)
        schedule.every().day.at("13:00").do(self.run_all_activities)
        schedule.every().day.at("17:00").do(self.run_all_activities)
        schedule.every().day.at("20:00").do(self.run_all_activities)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    bot = UnifiedSocialMediaBot()
    bot.start_scheduler()
