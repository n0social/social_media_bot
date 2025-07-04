import os
import time
import random
import schedule
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from instagrapi import Client
from pathlib import Path
import json
import requests
from pathlib import Path

class InstagramBot:
    def __init__(self):
        load_dotenv()
        self.setup_logging()
        
        # Instagram credentials removed for public release
        # self.username = os.getenv('INSTAGRAM_USERNAME')
        # self.password = os.getenv('INSTAGRAM_PASSWORD')
        
        # Bot configuration
        self.max_likes_per_hour = int(os.getenv('MAX_LIKES_PER_HOUR', 30))
        self.max_comments_per_hour = int(os.getenv('MAX_COMMENTS_PER_HOUR', 15))
        self.max_follows_per_hour = int(os.getenv('MAX_FOLLOWS_PER_HOUR', 20))
        self.post_interval_hours = int(os.getenv('POST_INTERVAL_HOURS', 24))
        
        # Content settings
        self.content_folder = os.getenv('CONTENT_FOLDER', 'content')
        self.hashtags = os.getenv('HASHTAGS', '#yesplease #socialmedia')
        
        # Safety settings
        self.enable_safety_delays = os.getenv('ENABLE_SAFETY_DELAYS', 'true').lower() == 'true'
        self.min_action_delay = int(os.getenv('MIN_ACTION_DELAY', 30))
        self.max_action_delay = int(os.getenv('MAX_ACTION_DELAY', 120))
        
        # Initialize client
        self.client = Client()
        
        # Activity tracking
        self.activity_log = {
            'likes_today': 0,
            'comments_today': 0,
            'follows_today': 0,
            'last_reset': datetime.now().date(),
            'last_post': None
        }
        
        self.load_activity_log()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('instagram_bot.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_activity_log(self):
        """Load activity log from file"""
        try:
            if os.path.exists('activity_log.json'):
                with open('activity_log.json', 'r') as f:
                    data = json.load(f)
                    self.activity_log.update(data)
                    # Convert string date back to date object
                    self.activity_log['last_reset'] = datetime.strptime(
                        self.activity_log['last_reset'], '%Y-%m-%d'
                    ).date()
        except Exception as e:
            self.logger.error(f"Error loading activity log: {e}")
            
    def save_activity_log(self):
        """Save activity log to file"""
        try:
            data = self.activity_log.copy()
            # Convert date to string for JSON serialization
            data['last_reset'] = data['last_reset'].strftime('%Y-%m-%d')
            with open('activity_log.json', 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Error saving activity log: {e}")
            
    def reset_daily_counters(self):
        """Reset daily activity counters if it's a new day"""
        today = datetime.now().date()
        if self.activity_log['last_reset'] < today:
            self.activity_log.update({
                'likes_today': 0,
                'comments_today': 0,
                'follows_today': 0,
                'last_reset': today
            })
            self.save_activity_log()
            self.logger.info("Daily activity counters reset")
            
    def login(self):
        """Login to Instagram"""
        try:
            self.logger.info(f"Attempting to login as {self.username}")
            self.client.login(self.username, self.password)
            self.logger.info("Successfully logged in to Instagram")
            return True
        except Exception as e:
            self.logger.error(f"Failed to login: {e}")
            return False
            
    def safe_delay(self):
        """Add random delay between actions for safety"""
        if self.enable_safety_delays:
            delay = random.randint(self.min_action_delay, self.max_action_delay)
            self.logger.info(f"Safety delay: {delay} seconds")
            time.sleep(delay)
            
    def can_perform_action(self, action_type):
        """Check if we can perform an action based on daily limits"""
        self.reset_daily_counters()
        
        limits = {
            'like': self.max_likes_per_hour,
            'comment': self.max_comments_per_hour,
            'follow': self.max_follows_per_hour
        }
        
        current_counts = {
            'like': self.activity_log['likes_today'],
            'comment': self.activity_log['comments_today'],
            'follow': self.activity_log['follows_today']
        }
        
        # Calculate hourly limit (assuming 16 active hours per day)
        daily_limit = limits[action_type] * 16
        
        return current_counts[action_type] < daily_limit
        
    def get_content_files(self):
        """Get list of content files to post"""
        content_path = Path(self.content_folder)
        if not content_path.exists():
            content_path.mkdir(exist_ok=True)
            self.logger.warning(f"Created content folder: {self.content_folder}")
            return []
            
        # Support common image formats
        image_extensions = ['.jpg', '.jpeg', '.png', '.mp4']
        content_files = []
        
        for ext in image_extensions:
            content_files.extend(content_path.glob(f"*{ext}"))
            
        return list(content_files)
        
    def create_post_caption(self, filename):
        """Create caption for post"""
        # Use an inspirational quote
        quotes = [
            "Believe you can and you're halfway there.",
            "Your only limit is your mind.",
            "Every day is a second chance.",
            "Start where you are. Use what you have. Do what you can.",
            "Dream big. Work hard. Stay focused.",
            "Small steps every day.",
            "You are stronger than you think.",
            "Progress, not perfection.",
            "Be the reason someone smiles today.",
            "Wellness is the natural state of my body."
        ]
        import random
        quote = random.choice(quotes)
        hashtags = self.hashtags
        # Compose caption: quote + hashtags
        return f"{quote}\n\n{hashtags}"
        
    def post_content(self):
        """Post content to Instagram"""
        try:
            # Inspirational quotes and matching Unsplash queries
            quote_image_pairs = [
                ("Believe you can and you're halfway there.", "mountain sunrise"),
                ("Your only limit is your mind.", "open road sky"),
                ("Every day is a second chance.", "fresh morning nature"),
                ("Start where you are. Use what you have. Do what you can.", "minimal workspace"),
                ("Dream big. Work hard. Stay focused.", "stars night sky"),
                ("Small steps every day.", "footsteps sand beach"),
                ("You are stronger than you think.", "strong athlete"),
                ("Progress, not perfection.", "growing plant"),
                ("Be the reason someone smiles today.", "smiling people"),
                ("Wellness is the natural state of my body.", "peaceful nature wellness"),
                ("Happiness is a journey, not a destination.", "happy journey travel"),
                ("Let your dreams be bigger than your fears.", "dream clouds sky"),
                ("You are enough just as you are.", "calm self care"),
                ("Gratitude turns what we have into enough.", "gratitude journal coffee"),
                ("Take care of your body. It's the only place you have to live.", "healthy food fitness"),
            ]
            import random
            quote, unsplash_query = random.choice(quote_image_pairs)
            images_folder = Path(self.content_folder) / "images"
            images_folder.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Fetching new image from Unsplash for query: {unsplash_query}")
            unsplash_img_path = fetch_unsplash_image(query=unsplash_query, save_folder=images_folder, logger=self.logger)
            if not unsplash_img_path:
                self.logger.error("Failed to fetch image from Unsplash")
                return False
            content_file = Path(unsplash_img_path)
            self.last_posted_file = str(content_file)
            caption = f"{quote}\n\n{self.hashtags}"

            # Ensure logged in before posting
            if not getattr(self.client, 'user_id', None):
                self.logger.info("Logging in to Instagram...")
                self.client.login(self.username, self.password)

            # Check if enough time has passed since last post
            if self.activity_log['last_post']:
                last_post_time = datetime.fromisoformat(self.activity_log['last_post'])
                time_since_last_post = datetime.now() - last_post_time
                if time_since_last_post.total_seconds() < (self.post_interval_hours * 3600):
                    self.logger.info("Not enough time passed since last post")
                    return False

            self.logger.info(f"Posting content: {content_file.name}")
            print(f"[InstagramBot] Posting content: {content_file.name}")
            # Post based on file type
            if content_file.suffix.lower() == '.mp4':
                media = self.client.video_upload(str(content_file), caption)
            else:
                media = self.client.photo_upload(str(content_file), caption)

            if media:
                self.activity_log['last_post'] = datetime.now().isoformat()
                self.save_activity_log()
                self.logger.info(f"Successfully posted content: {media.pk}")
                print(f"[InstagramBot] Successfully posted content: {media.pk}")
                return True
            else:
                self.logger.error("Failed to post content")
                print("[InstagramBot] Failed to post content")
                return False
        except Exception as e:
            self.logger.error(f"Error posting content: {e}")
            print(f"[InstagramBot] Error posting content: {e}")
            return False
            
    def like_recent_posts(self, hashtag, count=5):
        """Like recent posts with specific hashtag"""
        try:
            if not self.can_perform_action('like'):
                self.logger.info("Daily like limit reached")
                return
                
            self.logger.info(f"Looking for posts with hashtag: {hashtag}")
            medias = self.client.hashtag_medias_recent(hashtag, amount=count)
            
            for media in medias:
                if not self.can_perform_action('like'):
                    break
                    
                try:
                    self.client.media_like(media.id)
                    self.activity_log['likes_today'] += 1
                    self.logger.info(f"Liked post: {media.id}")
                    self.safe_delay()
                    
                except Exception as e:
                    self.logger.error(f"Error liking post {media.id}: {e}")
                    
            self.save_activity_log()
            
        except Exception as e:
            self.logger.error(f"Error in like_recent_posts: {e}")
            
    def comment_on_posts(self, hashtag, count=3):
        """Comment on recent posts with specific hashtag"""
        try:
            if not self.can_perform_action('comment'):
                self.logger.info("Daily comment limit reached")
                return
                
            comments = [
                "Great content! 🔥",
                "Love this! 💯",
                "Amazing post! 👏",
                "Awesome! 🚀",
                "Nice work! ✨",
                "So inspiring! 💪",
                "Perfect! 🎯"
            ]
            
            self.logger.info(f"Looking for posts to comment on with hashtag: {hashtag}")
            medias = self.client.hashtag_medias_recent(hashtag, amount=count)
            
            for media in medias:
                if not self.can_perform_action('comment'):
                    break
                    
                try:
                    comment_text = random.choice(comments)
                    self.client.media_comment(media.id, comment_text)
                    self.activity_log['comments_today'] += 1
                    self.logger.info(f"Commented on post: {media.id} - '{comment_text}'")
                    self.safe_delay()
                    
                except Exception as e:
                    self.logger.error(f"Error commenting on post {media.id}: {e}")
                    
            self.save_activity_log()
            
        except Exception as e:
            self.logger.error(f"Error in comment_on_posts: {e}")
            
    def follow_users(self, hashtag, count=2):
        """Follow users who posted with specific hashtag"""
        try:
            if not self.can_perform_action('follow'):
                self.logger.info("Daily follow limit reached")
                return
                
            self.logger.info(f"Looking for users to follow with hashtag: {hashtag}")
            medias = self.client.hashtag_medias_recent(hashtag, amount=count * 2)
            
            followed_count = 0
            for media in medias:
                if followed_count >= count or not self.can_perform_action('follow'):
                    break
                    
                try:
                    user_id = media.user.pk
                    self.client.user_follow(user_id)
                    self.activity_log['follows_today'] += 1
                    followed_count += 1
                    self.logger.info(f"Followed user: {media.user.username}")
                    self.safe_delay()
                    
                except Exception as e:
                    self.logger.error(f"Error following user {media.user.username}: {e}")
                    
            self.save_activity_log()
            
        except Exception as e:
            self.logger.error(f"Error in follow_users: {e}")
            
    def run_daily_activities(self):
        """Run all daily bot activities"""
        if not self.login():
            return
            
        try:
            self.logger.info("Starting daily Instagram bot activities")
            
            # Post content
            self.post_content()
            self.safe_delay()
            
            # Engage with content
            target_hashtags = ['socialmedia', 'content', 'instagram', 'marketing']
            
            for hashtag in target_hashtags:
                self.like_recent_posts(hashtag, count=3)
                self.comment_on_posts(hashtag, count=1)
                self.follow_users(hashtag, count=1)
                
            self.logger.info("Completed daily Instagram bot activities")
            
        except Exception as e:
            self.logger.error(f"Error in run_daily_activities: {e}")
        finally:
            try:
                self.client.logout()
            except:
                pass
                
    def start_scheduler(self):
        """Start the bot scheduler for continuous posting and engagement"""
        self.logger.info("Starting Instagram bot scheduler")
        print("[InstagramBot] Scheduler started. Monitoring and posting will continue...")
        schedule.every().day.at("10:00").do(self._notify_and_run)
        schedule.every().day.at("15:00").do(self._notify_and_run)
        schedule.every().day.at("19:00").do(self._notify_and_run)
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def _notify_and_run(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[InstagramBot] {now} - Running daily activities...")
        self.logger.info(f"[InstagramBot] {now} - Running daily activities...")
        result = self.run_daily_activities()
        if result is not False:
            print(f"[InstagramBot] {now} - Daily activities completed.")
        else:
            print(f"[InstagramBot] {now} - Daily activities failed or skipped.")

def fetch_unsplash_image(query="wellness", save_folder="content", logger=None):
    if logger is None:
        logger = logging.getLogger("instagram_bot")
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    url = f"https://api.unsplash.com/photos/random?query={query}&orientation=squarish&client_id={access_key}"
    response = requests.get(url)
    logger.info(f"Unsplash API request URL: {url}")
    logger.info(f"Unsplash API response status: {response.status_code}")
    try:
        logger.info(f"Unsplash API response: {response.text}")
    except Exception:
        pass
    if response.status_code == 200:
        data = response.json()
        if 'urls' not in data or 'regular' not in data['urls']:
            logger.error(f"Unsplash API response missing image URL: {data}")
            return None
        img_url = data['urls']['regular']
        img_data = requests.get(img_url).content
        img_path = Path(save_folder) / f"unsplash_{query}_{data['id']}.jpg"
        with open(img_path, 'wb') as f:
            f.write(img_data)
        return img_path
    else:
        logger.error(f"Failed to fetch from Unsplash: {response.status_code} {response.text}")
        return None

if __name__ == "__main__":
    bot = InstagramBot()
    bot.start_scheduler()
