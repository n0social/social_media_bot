import os
import time
import random
import schedule
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv
from pathlib import Path
import json

# Import individual bots
try:
    from instagram_bot import InstagramBot
    INSTAGRAM_AVAILABLE = True
except ImportError:
    INSTAGRAM_AVAILABLE = False
    print("⚠️  Instagram bot not available")

try:
    from x_bot import XBot
    X_AVAILABLE = True
except ImportError:
    X_AVAILABLE = False
    print("⚠️  X bot not available")

class SocialMediaBot:
    """Unified social media bot for Instagram and X"""
    
    def __init__(self):
        load_dotenv()
        self.setup_logging()
        self.load_configuration()

        # Activity tracking (must be before initialize_bots)
        self.activity_tracker = {
            'session_start': datetime.now(),
            'platforms_active': [],
            'daily_stats': {},
            'last_activity_reset': datetime.now().date()
        }

        # Initialize individual bots
        self.instagram_bot = None
        self.x_bot = None
        self.initialize_bots()

        self.load_activity_data()
        
    def setup_logging(self):
        """Setup logging for unified bot"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(logs_dir / 'social_media_bot.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger('SocialMediaBot')
        
    def load_configuration(self):
        """Load configuration for both platforms"""
        # Platform settings
        self.instagram_enabled = os.getenv('ENABLE_INSTAGRAM', 'true').lower() == 'true'
        self.x_enabled = os.getenv('ENABLE_X', 'true').lower() == 'true'
        
        # Content settings
        self.content_folder = Path(os.getenv('CONTENT_FOLDER', 'content'))
        self.post_interval_hours = int(os.getenv('POST_INTERVAL_HOURS', 24))
        
        # Safety settings
        self.max_daily_posts = int(os.getenv('MAX_POSTS_PER_DAY', 10))
        self.enable_cross_posting = os.getenv('ENABLE_CROSS_POSTING', 'true').lower() == 'true'
        
        self.logger.info(f"Social Media Bot configured - Instagram: {self.instagram_enabled}, X: {self.x_enabled}")
        
    def initialize_bots(self):
        """Initialize individual platform bots"""
        if self.instagram_enabled and INSTAGRAM_AVAILABLE:
            try:
                self.instagram_bot = InstagramBot()
                self.activity_tracker['platforms_active'].append('Instagram')
                self.logger.info("Instagram bot initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize Instagram bot: {e}")
                
        if self.x_enabled and X_AVAILABLE:
            try:
                self.x_bot = XBot()
                self.activity_tracker['platforms_active'].append('X')
                self.logger.info("X bot initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize X bot: {e}")
                
    def load_activity_data(self):
        """Load activity tracking data"""
        try:
            activity_file = Path('data/social_media_activity.json')
            if activity_file.exists():
                with open(activity_file, 'r') as f:
                    data = json.load(f)
                    self.activity_tracker.update(data)
                    
                # Convert date strings back to date objects
                if 'last_activity_reset' in self.activity_tracker:
                    self.activity_tracker['last_activity_reset'] = datetime.strptime(
                        self.activity_tracker['last_activity_reset'], '%Y-%m-%d'
                    ).date()
                    
                if 'session_start' in self.activity_tracker:
                    self.activity_tracker['session_start'] = datetime.fromisoformat(
                        self.activity_tracker['session_start']
                    )
                    
        except Exception as e:
            self.logger.error(f"Error loading social media activity data: {e}")
            
    def save_activity_data(self):
        """Save activity tracking data"""
        try:
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            
            # Convert datetime objects to strings for JSON
            save_data = self.activity_tracker.copy()
            if 'last_activity_reset' in save_data:
                save_data['last_activity_reset'] = save_data['last_activity_reset'].strftime('%Y-%m-%d')
            if 'session_start' in save_data:
                save_data['session_start'] = save_data['session_start'].isoformat()
                
            with open(data_dir / 'social_media_activity.json', 'w') as f:
                json.dump(save_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving social media activity data: {e}")
            
    def reset_daily_counters(self):
        """Reset daily activity counters if needed"""
        today = datetime.now().date()
        
        if self.activity_tracker['last_activity_reset'] < today:
            self.activity_tracker['daily_stats'] = {}
            self.activity_tracker['last_activity_reset'] = today
            self.save_activity_data()
            self.logger.info("Daily social media counters reset")
            
    def get_content_to_post(self) -> Optional[Path]:
        """Get content to post (shared between platforms)"""
        if not self.content_folder.exists():
            self.logger.warning(f"Content folder {self.content_folder} does not exist")
            return None
            
        # Get all content files
        content_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.mp4']:
            content_files.extend(self.content_folder.glob(f"*{ext}"))
            
        if not content_files:
            self.logger.warning("No content files found")
            return None
            
        # Return random content file
        return random.choice(content_files)
        
    def post_to_instagram(self) -> bool:
        """Post content to Instagram"""
        if not self.instagram_bot:
            self.logger.warning("Instagram bot not available")
            return False
            
        try:
            success = self.instagram_bot.post_content()
            if success:
                # Log post details
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                last_post = self.instagram_bot.activity_log.get('last_post', now)
                content_file = getattr(self.instagram_bot, 'last_posted_file', None)
                self.logger.info(f"[POSTED] Platform: Instagram | Time: {last_post} | Content: {content_file if content_file else 'N/A'}")
                self.record_activity('instagram_post')
                self.logger.info("Successfully posted to Instagram")
            return success
            
        except Exception as e:
            self.logger.error(f"Error posting to Instagram: {e}")
            return False
            
    def post_to_x(self) -> bool:
        """Post content to X"""
        if not self.x_bot:
            self.logger.warning("X bot not available")
            return False
            
        try:
            content = self.x_bot.create_post_content()
            success = self.x_bot.post_to_x(content)
            if success:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.logger.info(f"[POSTED] Platform: X | Time: {now} | Content: {content}")
                self.record_activity('x_post')
                self.logger.info("Successfully posted to X")
            return success
            
        except Exception as e:
            self.logger.error(f"Error posting to X: {e}")
            return False
            
    def cross_post_content(self) -> Dict[str, bool]:
        """Post content to all enabled platforms"""
        results = {}
        
        # Determine which platforms to post to
        platforms_to_post = []
        
        if self.instagram_enabled and self.instagram_bot:
            platforms_to_post.append('instagram')
            
        if self.x_enabled and self.x_bot:
            platforms_to_post.append('x')
            
        if not platforms_to_post:
            self.logger.warning("No platforms available for posting")
            return results
            
        # Post to platforms
        for platform in platforms_to_post:
            try:
                if platform == 'instagram':
                    results['instagram'] = self.post_to_instagram()
                elif platform == 'x':
                    results['x'] = self.post_to_x()
                    
                # Add delay between platform posts
                if len(platforms_to_post) > 1:
                    delay = random.randint(60, 180)  # 1-3 minutes between platforms
                    self.logger.info(f"Cross-posting delay: {delay} seconds")
                    time.sleep(delay)
                    
            except Exception as e:
                self.logger.error(f"Error posting to {platform}: {e}")
                results[platform] = False
                
        return results
        
    def run_instagram_engagement(self):
        """Run Instagram engagement activities"""
        if not self.instagram_bot:
            return
            
        try:
            self.logger.info("Running Instagram engagement activities")
            
            # Like posts
            hashtags = ['socialmedia', 'digitalmarketing', 'entrepreneur', 'business']
            for hashtag in hashtags[:2]:
                self.instagram_bot.like_recent_posts(hashtag, count=2)
                
            # Comment on posts
            for hashtag in hashtags[:1]:
                self.instagram_bot.comment_on_posts(hashtag, count=1)
                
            self.logger.info("Completed Instagram engagement activities")
            
        except Exception as e:
            self.logger.error(f"Error in Instagram engagement: {e}")
            
    def run_x_engagement(self):
        """Run X engagement activities"""
        if not self.x_bot:
            return
            
        try:
            self.logger.info("Running X engagement activities")
            
            # Like posts
            search_terms = ['social media marketing', 'digital marketing', 'business growth']
            for term in search_terms[:2]:
                self.x_bot.like_posts(term, count=2)
                
            # Repost content
            for term in search_terms[:1]:
                self.x_bot.repost_content(term, count=1)
                
            self.logger.info("Completed X engagement activities")
            
        except Exception as e:
            self.logger.error(f"Error in X engagement: {e}")
            
    def run_daily_activities(self):
        """Run all daily social media activities"""
        self.reset_daily_counters()
        
        try:
            self.logger.info("Starting daily social media activities")
            
            # Cross-post content
            if self.enable_cross_posting:
                post_results = self.cross_post_content()
                self.logger.info(f"Cross-posting results: {post_results}")
            else:
                # Post to platforms individually
                if self.instagram_enabled:
                    self.post_to_instagram()
                if self.x_enabled:
                    self.post_to_x()
                    
            # Add delay before engagement activities
            time.sleep(random.randint(300, 600))  # 5-10 minutes
            
            # Run engagement activities
            self.run_instagram_engagement()
            self.run_x_engagement()
            
            self.logger.info("Completed daily social media activities")
            
        except Exception as e:
            self.logger.error(f"Error in daily activities: {e}")
            
    def record_activity(self, activity_type: str):
        """Record activity across platforms"""
        if activity_type not in self.activity_tracker['daily_stats']:
            self.activity_tracker['daily_stats'][activity_type] = 0
        self.activity_tracker['daily_stats'][activity_type] += 1
        
        self.save_activity_data()
        self.logger.info(f"Recorded activity: {activity_type}")
        
    def get_unified_summary(self) -> Dict:
        """Get unified activity summary"""
        summary = {
            'platforms_active': self.activity_tracker['platforms_active'],
            'session_start': self.activity_tracker['session_start'],
            'daily_stats': self.activity_tracker['daily_stats'],
            'instagram_enabled': self.instagram_enabled,
            'x_enabled': self.x_enabled,
            'cross_posting_enabled': self.enable_cross_posting
        }
        
        # Add individual bot summaries
        if self.instagram_bot:
            summary['instagram_summary'] = self.instagram_bot.get_activity_summary()
            
        if self.x_bot:
            summary['x_summary'] = self.x_bot.get_activity_summary()
            
        return summary
        
    def start_scheduler(self):
        """Start the unified social media bot scheduler"""
        self.logger.info("Starting unified social media bot scheduler")
        
        # Schedule daily activities
        schedule.every().day.at("09:00").do(self.run_daily_activities)
        schedule.every().day.at("13:00").do(self.run_daily_activities)
        schedule.every().day.at("17:00").do(self.run_daily_activities)
        schedule.every().day.at("20:00").do(self.run_daily_activities)
        
        # Schedule engagement-only activities
        schedule.every().day.at("11:00").do(self.run_instagram_engagement)
        schedule.every().day.at("15:00").do(self.run_x_engagement)
        schedule.every().day.at("19:00").do(self.run_instagram_engagement)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        bot = SocialMediaBot()
        print("🚀 Unified Social Media Bot initialized!")
        print("=" * 50)
        
        summary = bot.get_unified_summary()
        print(f"Active platforms: {summary['platforms_active']}")
        print(f"Instagram enabled: {summary['instagram_enabled']}")
        print(f"X enabled: {summary['x_enabled']}")
        print(f"Cross-posting enabled: {summary['cross_posting_enabled']}")
        
        # Start scheduler
        bot.start_scheduler()
        
    except KeyboardInterrupt:
        print("\n⏹️  Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
