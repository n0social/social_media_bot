import os
import time
import random
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from pathlib import Path

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, ChallengeRequired, RateLimitError
except ImportError:
    print("⚠️  instagrapi not installed. Run: pip install -r requirements.txt")
    Client = None

from bot_config import BotConfig, SafetyChecker

class AdvancedInstagramBot:
    """Advanced Instagram bot with enhanced safety and features"""
    
    def __init__(self):
        load_dotenv()
        self.setup_logging()
        self.load_configuration()
        
        # Initialize safety checker
        self.safety_checker = SafetyChecker()
        
        # Initialize client
        if Client:
            self.client = Client()
        else:
            self.client = None
            self.logger.error("Instagram client not available")
            
        # Activity tracking
        self.activity_tracker = {
            'session_start': None,
            'actions_this_hour': {},
            'daily_stats': {},
            'last_activity_reset': datetime.now().date()
        }
        
        self.load_activity_data()
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Create logs directory
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(logs_dir / 'bot.log'),
                logging.FileHandler(logs_dir / 'errors.log', mode='a'),
                logging.StreamHandler()
            ]
        )
        
        # Separate error logger
        error_handler = logging.FileHandler(logs_dir / 'errors.log')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(log_format))
        
        self.logger = logging.getLogger(__name__)
        self.error_logger = logging.getLogger('errors')
        self.error_logger.addHandler(error_handler)
        
    def load_configuration(self):
        """Load bot configuration from environment and config"""
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError("Instagram credentials not found in .env file")
            
        # Bot settings with defaults
        self.content_folder = Path(os.getenv('CONTENT_FOLDER', 'content'))
        self.enable_posting = os.getenv('ENABLE_POSTING', 'true').lower() == 'true'
        self.enable_engagement = os.getenv('ENABLE_ENGAGEMENT', 'true').lower() == 'true'
        self.dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
        
        self.logger.info(f"Bot configured - Posting: {self.enable_posting}, Engagement: {self.enable_engagement}")
        
    def load_activity_data(self):
        """Load activity tracking data"""
        try:
            activity_file = Path('data/activity_tracker.json')
            if activity_file.exists():
                with open(activity_file, 'r') as f:
                    data = json.load(f)
                    self.activity_tracker.update(data)
                    
                # Convert date strings back to date objects
                if 'last_activity_reset' in self.activity_tracker:
                    self.activity_tracker['last_activity_reset'] = datetime.strptime(
                        self.activity_tracker['last_activity_reset'], '%Y-%m-%d'
                    ).date()
        except Exception as e:
            self.logger.error(f"Error loading activity data: {e}")
            
    def save_activity_data(self):
        """Save activity tracking data"""
        try:
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            
            # Convert date objects to strings for JSON
            save_data = self.activity_tracker.copy()
            if 'last_activity_reset' in save_data:
                save_data['last_activity_reset'] = save_data['last_activity_reset'].strftime('%Y-%m-%d')
                
            with open(data_dir / 'activity_tracker.json', 'w') as f:
                json.dump(save_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving activity data: {e}")
            
    def reset_hourly_counters(self):
        """Reset hourly activity counters"""
        current_hour = datetime.now().hour
        
        # Reset if we're in a new hour
        if not hasattr(self, '_last_hour_reset') or self._last_hour_reset != current_hour:
            self.activity_tracker['actions_this_hour'] = {}
            self._last_hour_reset = current_hour
            self.logger.info("Hourly counters reset")
            
    def reset_daily_counters(self):
        """Reset daily activity counters if needed"""
        today = datetime.now().date()
        
        if self.activity_tracker['last_activity_reset'] < today:
            self.activity_tracker['daily_stats'] = {}
            self.activity_tracker['last_activity_reset'] = today
            self.safety_checker.reset_daily_counters()
            self.save_activity_data()
            self.logger.info("Daily counters reset")
            
    def safe_login(self) -> bool:
        """Safely login to Instagram with error handling"""
        if not self.client:
            self.logger.error("Instagram client not available")
            return False
            
        try:
            self.logger.info(f"Attempting login for {self.username}")
            
            # Check for existing session
            session_file = Path('data/session.json')
            if session_file.exists():
                try:
                    self.client.load_settings(session_file)
                    self.client.login(self.username, self.password)
                    self.logger.info("Logged in using saved session")
                    return True
                except:
                    self.logger.info("Saved session invalid, logging in fresh")
                    
            # Fresh login
            self.client.login(self.username, self.password)
            
            # Save session
            session_file.parent.mkdir(exist_ok=True)
            self.client.dump_settings(session_file)
            
            self.safety_checker.start_session()
            self.logger.info("Successfully logged in and session saved")
            return True
            
        except ChallengeRequired as e:
            self.error_logger.error(f"Challenge required: {e}")
            self.logger.error("Instagram requires verification. Please login manually first.")
            return False
            
        except RateLimitError as e:
            self.error_logger.error(f"Rate limit error: {e}")
            self.logger.error("Rate limited. Waiting before retry...")
            time.sleep(BotConfig.DELAYS['error_delay'])
            return False
            
        except Exception as e:
            self.error_logger.error(f"Login failed: {e}")
            self.safety_checker.record_error()
            return False
            
    def safe_logout(self):
        """Safely logout from Instagram"""
        try:
            if self.client:
                self.client.logout()
                self.safety_checker.end_session()
                self.logger.info("Successfully logged out")
        except Exception as e:
            self.logger.error(f"Error during logout: {e}")
            
    def get_random_delay(self, min_delay: int = None, max_delay: int = None) -> int:
        """Get random delay for human-like behavior"""
        min_delay = min_delay or BotConfig.DELAYS['min_action_delay']
        max_delay = max_delay or BotConfig.DELAYS['max_action_delay']
        
        return random.randint(min_delay, max_delay)
        
    def human_delay(self, action_type: str = 'general'):
        """Add human-like delay between actions"""
        if action_type == 'post':
            delay = self.get_random_delay(
                BotConfig.DELAYS['post_delay'],
                BotConfig.DELAYS['post_delay'] + 300
            )
        elif action_type == 'error':
            delay = BotConfig.DELAYS['error_delay']
        else:
            delay = self.get_random_delay()
            
        self.logger.info(f"Human delay: {delay} seconds ({action_type})")
        time.sleep(delay)
        
    def can_perform_action(self, action_type: str) -> Tuple[bool, str]:
        """Check if an action can be performed safely"""
        self.reset_hourly_counters()
        self.reset_daily_counters()
        
        # Get current hour's count for this action
        current_count = self.activity_tracker['actions_this_hour'].get(action_type, 0)
        
        # Use safety checker
        can_perform, reason = self.safety_checker.can_perform_action(action_type, current_count)
        
        if not can_perform:
            self.logger.warning(f"Cannot perform {action_type}: {reason}")
            
        return can_perform, reason
        
    def record_action(self, action_type: str):
        """Record that an action was performed"""
        # Update hourly counter
        if action_type not in self.activity_tracker['actions_this_hour']:
            self.activity_tracker['actions_this_hour'][action_type] = 0
        self.activity_tracker['actions_this_hour'][action_type] += 1
        
        # Update daily stats
        if action_type not in self.activity_tracker['daily_stats']:
            self.activity_tracker['daily_stats'][action_type] = 0
        self.activity_tracker['daily_stats'][action_type] += 1
        
        # Update safety checker
        self.safety_checker.record_action()
        
        # Save data
        self.save_activity_data()
        
        self.logger.info(f"Action recorded: {action_type}")
        
    def get_content_to_post(self) -> Optional[Path]:
        """Get next content file to post"""
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
            
        # Load posting history
        history_file = Path('data/post_history.json')
        posted_files = []
        
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    posted_files = json.load(f).get('posted_files', [])
            except:
                pass
                
        # Find unposted files
        unposted_files = [f for f in content_files if f.name not in posted_files]
        
        if not unposted_files:
            # All files posted, reset history
            posted_files = []
            unposted_files = content_files
            self.logger.info("All content posted, resetting rotation")
            
        # Select random unposted file
        selected_file = random.choice(unposted_files)
        
        # Update history
        posted_files.append(selected_file.name)
        history_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(history_file, 'w') as f:
                json.dump({'posted_files': posted_files}, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error updating post history: {e}")
            
        return selected_file
        
    def create_post_caption(self, content_file: Path) -> str:
        """Create engaging caption for post"""
        # Base caption options
        caption_templates = [
            "Excited to share this with you! 🚀",
            "Hope this brightens your day! ✨",
            "What do you think about this? 💭",
            "Sharing some inspiration! 💪",
            "Another day, another opportunity! 🌟"
        ]
        
        base_caption = random.choice(caption_templates)
        
        # Add hashtags
        hashtags = " ".join(BotConfig.CONTENT['hashtags'])
        
        # Add call to action
        cta_options = [
            "\n\nWhat's your favorite part? Tell us below! 👇",
            "\n\nDouble tap if you agree! ❤️",
            "\n\nTag someone who needs to see this! 👥",
            "\n\nSave this for later! 📌"
        ]
        
        cta = random.choice(cta_options)
        
        return f"{base_caption}\n\n{hashtags}{cta}"
        
    def post_content(self) -> bool:
        """Post content to Instagram"""
        if not self.enable_posting:
            self.logger.info("Posting disabled in configuration")
            return False
            
        if not self.can_perform_action('post')[0]:
            return False
            
        try:
            content_file = self.get_content_to_post()
            if not content_file:
                return False
                
            caption = self.create_post_caption(content_file)
            
            if self.dry_run:
                self.logger.info(f"DRY RUN: Would post {content_file.name}")
                return True
                
            self.logger.info(f"Posting content: {content_file.name}")
            
            # Post based on file type
            if content_file.suffix.lower() == '.mp4':
                media = self.client.video_upload(str(content_file), caption)
            else:
                media = self.client.photo_upload(str(content_file), caption)
                
            if media:
                self.record_action('post')
                self.logger.info(f"Successfully posted: {media.pk}")
                self.human_delay('post')
                return True
            else:
                self.logger.error("Failed to post content")
                return False
                
        except Exception as e:
            self.error_logger.error(f"Error posting content: {e}")
            self.safety_checker.record_error()
            self.human_delay('error')
            return False
            
    def get_activity_summary(self) -> Dict:
        """Get summary of bot activities"""
        self.reset_hourly_counters()
        self.reset_daily_counters()
        
        return {
            'today': self.activity_tracker['daily_stats'],
            'this_hour': self.activity_tracker['actions_this_hour'],
            'session_active': self.safety_checker.session_start is not None
        }

# Example usage and testing
if __name__ == "__main__":
    try:
        bot = AdvancedInstagramBot()
        
        # Test basic functionality
        print("Bot initialized successfully!")
        print("Activity summary:", bot.get_activity_summary())
        
        # Test login (comment out for actual use)
        # if bot.safe_login():
        #     print("Login successful!")
        #     bot.safe_logout()
        
    except Exception as e:
        print(f"Error initializing bot: {e}")
