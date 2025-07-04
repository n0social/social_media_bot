import os
import time
import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from pathlib import Path
import json

try:
    import tweepy
except ImportError:
    print("⚠️  tweepy not installed. Run: pip install -r requirements.txt")
    tweepy = None

from bot_config import BotConfig, SafetyChecker

class XBot:
    """X bot for automated posting and engagement (credentials removed for public release)"""
    
    def __init__(self):
        load_dotenv()
        self.setup_logging()
        self.load_configuration()
        
        # Initialize safety checker
        self.safety_checker = SafetyChecker()
        
        # Initialize X client (disabled for public release)
        self.client = None
        self.api = None
        # self.setup_x_client()  # Disabled
        
        # Activity tracking
        self.activity_tracker = {
            'session_start': None,
            'actions_this_hour': {},
            'daily_stats': {},
            'last_activity_reset': datetime.now().date()
        }
        
        self.load_activity_data()
        
    def setup_logging(self):
        """Setup logging for X bot"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/x_bot.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger('XBot')
        
    def load_configuration(self):
        """Load X configuration from environment (credentials removed)"""
        # X API credentials removed for public release
        # self.api_key = os.getenv('X_API_KEY')
        # self.api_secret = os.getenv('X_API_SECRET')
        # self.access_token = os.getenv('X_ACCESS_TOKEN')
        # self.access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
        # self.bearer_token = os.getenv('X_BEARER_TOKEN')
        
        # Bot settings
        self.max_tweets_per_day = int(os.getenv('MAX_TWEETS_PER_DAY', 10))
        self.max_retweets_per_hour = int(os.getenv('MAX_RETWEETS_PER_HOUR', 20))
        self.max_likes_per_hour = int(os.getenv('MAX_LIKES_PER_HOUR', 30))
        
        # Content settings
        self.content_folder = Path(os.getenv('CONTENT_FOLDER', 'content'))
        self.x_hashtags = os.getenv('X_HASHTAGS', '#YesPlease #SocialMedia #Content #X')
        
        # Platform settings
        self.enabled = os.getenv('ENABLE_X', 'true').lower() == 'true'
        
        self.logger.info(f"X bot configured - Enabled: {self.enabled}")
        
    # def setup_x_client(self):
    #     """Setup X API client (disabled for public release)"""
    #     pass

    def load_activity_data(self):
        """Load activity tracking data"""
        try:
            activity_file = Path('data/x_activity.json')
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
            self.logger.error(f"Error loading X activity data: {e}")
            
    def save_activity_data(self):
        """Save activity tracking data"""
        try:
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            
            # Convert date objects to strings for JSON
            save_data = self.activity_tracker.copy()
            if 'last_activity_reset' in save_data:
                save_data['last_activity_reset'] = save_data['last_activity_reset'].strftime('%Y-%m-%d')
                
            with open(data_dir / 'x_activity.json', 'w') as f:
                json.dump(save_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving X activity data: {e}")
            
    def reset_daily_counters(self):
        """Reset daily activity counters if needed"""
        today = datetime.now().date()
        
        if self.activity_tracker['last_activity_reset'] < today:
            self.activity_tracker['daily_stats'] = {}
            self.activity_tracker['last_activity_reset'] = today
            self.save_activity_data()
            self.logger.info("Daily X counters reset")
            
    def reset_hourly_counters(self):
        """Reset hourly activity counters"""
        current_hour = datetime.now().hour
        
        if not hasattr(self, '_last_hour_reset') or self._last_hour_reset != current_hour:
            self.activity_tracker['actions_this_hour'] = {}
            self._last_hour_reset = current_hour
            self.logger.info("Hourly X counters reset")
            
    def can_perform_action(self, action_type: str) -> Tuple[bool, str]:
        """Check if an action can be performed safely"""
        if not self.enabled:
            return False, "X bot disabled"
            
        self.reset_hourly_counters()
        self.reset_daily_counters()
        
        # Get current counts
        hourly_count = self.activity_tracker['actions_this_hour'].get(action_type, 0)
        daily_count = self.activity_tracker['daily_stats'].get(action_type, 0)
        
        # Check limits
        if action_type == 'tweet' and daily_count >= self.max_tweets_per_day:
            return False, "Daily tweet limit reached"
            
        if action_type == 'like' and hourly_count >= self.max_likes_per_hour:
            return False, "Hourly like limit reached"
            
        if action_type == 'retweet' and hourly_count >= self.max_retweets_per_hour:
            return False, "Hourly retweet limit reached"
            
        return True, "OK"
        
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
        
        # Save data
        self.save_activity_data()
        self.logger.info(f"X action recorded: {action_type}")
        
    def human_delay(self):
        """Add human-like delay between actions"""
        delay = random.randint(30, 120)
        self.logger.info(f"X delay: {delay} seconds")
        time.sleep(delay)
        
    def create_post_content(self, content_type: str = 'general') -> str:
        """Create engaging post content for X"""
        post_templates = {
            'mental_health': [
                "Your mental health is a priority. Take time for yourself today. 💚",
                "Healing is not linear. Be gentle with yourself on the journey.",
                "You are enough, just as you are. #SelfAcceptance 🙏",
                "It's okay to rest. Your mind and soul need it, too. 💤",
                "Progress is progress, no matter how small. #KeepGoing 🐢",
                "You are not alone. Reach out, connect, and share. #SupportEachOther 🤝",
                "Breathe in calm, breathe out stress. #Mindfulness 🌬️",
                "Let go of what you can't control. Embrace the present moment. 🕊️",
                "Self-care is not selfish. It's essential. #SelfCare 🛁",
                "Your story matters. Every chapter, every feeling. #MentalHealthMatters 📖"
            ],
            'spirituality': [
                "Nourish your soul with gratitude and kindness. ✨",
                "Trust the timing of your life. The universe has a plan. 🌌",
                "Stillness is where clarity lives. Take a mindful pause. 🧘‍♂️",
                "Let your light shine, even on the darkest days. 🕯️",
                "You are a unique expression of the universe. #Oneness 🌠",
                "Peace begins within. Center yourself and radiate calm. 🧘‍♀️",
                "Listen to your intuition. It knows the way. 👂✨",
                "Release what no longer serves you. Make space for growth. 🍃",
                "Every breath is a new beginning. #Presence 🌱",
                "Connect with your higher self. Trust your journey. 🦋"
            ],
            'wellness': [
                "Wellness is a daily practice, not a destination. #HealthyHabits 🏃‍♂️",
                "Hydrate, nourish, move, rest. Repeat. #WellnessRoutine 💧🥗🧘‍♂️😴",
                "Celebrate small wins on your wellness journey. 🎉",
                "Balance is not something you find, it's something you create. ⚖️",
                "A healthy mind supports a healthy body. #HolisticHealth 🧠💪",
                "Gratitude is the best medicine. #Thankful 🙏",
                "Let nature restore your spirit. Take a mindful walk today. 🌳🚶‍♀️",
                "Boundaries are a form of self-respect. Set them with love. 🛑❤️",
                "Rest is productive. Give yourself permission to recharge. 🔋",
                "You are worthy of wellness and joy. 🌞"
            ],
            'engagement': [
                "What's one thing you do for your mental well-being? Share below! 💬",
                "How do you practice mindfulness in your daily life? 🧘‍♀️",
                "Share a quote or mantra that inspires you! ✨",
                "What helps you feel grounded and present? 🌳",
                "Tag someone who brings positivity to your life! 🌟",
                "What's your favorite self-care ritual? 🛁",
                "How do you stay connected to your purpose? 🎯",
                "What's one thing you're grateful for today? 🙏",
                "How do you recharge your energy? 🔋",
                "What's your go-to for finding inner peace? 🕊️",
                "Consent is fun! Respect and joy go hand in hand. 🎉🕺💃",
                "Celebrate your boundaries—they make connection possible! 🎆",
                "Grateful for the little things: a smile, a song, a sunrise. 🌅😊🎶",
                "Dance like nobody's watching and bow to your own joy! 💃🕺🙇‍♂️",
                "Fireworks of gratitude for everyone who supports me! 🎆🙏",
                "What are you celebrating today? Share your wins! 🎉🥳",
                "Thank you, universe, for another day to grow and love. 🌌💖",
                "Let's spread kindness like confetti! 🎊",
                "Bow to your journey—every step matters. 🙇‍♀️✨",
                "Who or what are you grateful for right now? Tag them! 🙏💫"
            ]
        }
        
        # Select random template from category
        templates = post_templates.get(content_type, post_templates['engagement'])
        base_post = random.choice(templates)
        
        # Add hashtags
        hashtags = self.x_hashtags
        
        # Ensure post is under 280 characters (X character limit)
        full_post = f"{base_post}\n\n{hashtags}"
        
        if len(full_post) > 280:
            # Truncate hashtags if needed
            available_space = 280 - len(base_post) - 3  # 3 for "\n\n"
            if available_space > 0:
                hashtags = hashtags[:available_space]
                full_post = f"{base_post}\n\n{hashtags}"
            else:
                full_post = base_post[:277] + "..."
                
        return full_post
        
    def post_to_x(self, content: str = None) -> bool:
        """Post to X"""
        can_post, reason = self.can_perform_action('tweet')
        if not can_post:
            self.logger.info(f"Skipping X post: {reason}")
            return False
            
        try:
            if not content:
                content = self.create_post_content()
                
            self.logger.info(f"Attempting to post to X. Content: {content}")
            
            # Post to X
            response = self.client.create_tweet(text=content)
            self.logger.info(f"X API response: {getattr(response, 'data', None)} | Full: {response}")
            
            if response.data:
                self.record_action('tweet')
                self.logger.info(f"Successfully posted to X: {response.data['id']}")
                self.human_delay()
                return True
            else:
                self.logger.error(f"Failed to post to X. Response: {response}")
                return False
                
        except Exception as e:
            import traceback
            self.logger.error(f"Error posting to X: {e}\n{traceback.format_exc()}")
            return False
            
    def like_posts(self, search_term: str, count: int = 5) -> int:
        """Like posts containing search term"""
        if not self.can_perform_action('like')[0]:
            return 0
            
        liked_count = 0
        
        try:
            self.logger.info(f"Searching for posts with: {search_term}")
            
            # Search for posts
            posts = self.client.search_recent_tweets(
                query=f"{search_term} -is:retweet lang:en",
                max_results=min(count * 2, 100),
                tweet_fields=['author_id', 'created_at', 'public_metrics']
            )
            
            if not posts.data:
                self.logger.info("No posts found to like")
                return 0
                
            for post in posts.data[:count]:
                if not self.can_perform_action('like')[0]:
                    break
                    
                try:
                    # Like the post
                    self.client.like(post.id)
                    self.record_action('like')
                    liked_count += 1
                    self.logger.info(f"Liked post: {post.id}")
                    self.human_delay()
                    
                except Exception as e:
                    self.logger.error(f"Error liking post {post.id}: {e}")
                    
            return liked_count
            
        except Exception as e:
            self.logger.error(f"Error in like_posts: {e}")
            return 0
            
    def repost_content(self, search_term: str, count: int = 3) -> int:
        """Repost content containing search term"""
        if not self.can_perform_action('repost')[0]:
            return 0
            
        reposted_count = 0
        
        try:
            self.logger.info(f"Searching for posts to repost: {search_term}")
            
            # Search for posts
            posts = self.client.search_recent_tweets(
                query=f"{search_term} -is:retweet lang:en",
                max_results=min(count * 3, 100),
                tweet_fields=['author_id', 'created_at', 'public_metrics']
            )
            
            if not posts.data:
                self.logger.info("No posts found to repost")
                return 0
                
            for post in posts.data[:count]:
                if not self.can_perform_action('repost')[0]:
                    break
                    
                try:
                    # Check if post has good engagement
                    metrics = post.public_metrics
                    if metrics['like_count'] > 5 or metrics['retweet_count'] > 2:
                        self.client.retweet(post.id)
                        self.record_action('repost')
                        reposted_count += 1
                        self.logger.info(f"Reposted: {post.id}")
                        self.human_delay()
                    
                except Exception as e:
                    self.logger.error(f"Error reposting {post.id}: {e}")
                    
            return reposted_count
            
        except Exception as e:
            self.logger.error(f"Error in repost_content: {e}")
            return 0
            
    def follow_users(self, search_term: str, count: int = 2) -> int:
        """Follow users who post about search term"""
        followed_count = 0
        
        try:
            self.logger.info(f"Looking for users to follow: {search_term}")
            
            # Search for posts
            posts = self.client.search_recent_tweets(
                query=f"{search_term} -is:retweet lang:en",
                max_results=min(count * 3, 100),
                tweet_fields=['author_id'],
                expansions=['author_id'],
                user_fields=['public_metrics']
            )
            
            if not posts.data or not posts.includes.get('users'):
                self.logger.info("No users found to follow")
                return 0
                
            for user in posts.includes['users'][:count]:
                try:
                    # Check user metrics
                    metrics = user.public_metrics
                    followers = metrics['followers_count']
                    following = metrics['following_count']
                    
                    # Follow users with reasonable follower ratios
                    if 100 <= followers <= 10000 and following < followers * 2:
                        self.client.follow_user(user.id)
                        followed_count += 1
                        self.logger.info(f"Followed user: @{user.username}")
                        self.human_delay()
                        
                except Exception as e:
                    self.logger.error(f"Error following user {user.username}: {e}")
                    
            return followed_count
            
        except Exception as e:
            self.logger.error(f"Error in follow_users: {e}")
            return 0
            
    def run_daily_activities(self):
        """Run all daily X bot activities"""
        if not self.enabled:
            self.logger.info("X bot disabled")
            return
            
        if not self.client:
            self.logger.error("X client not available")
            return
            
        try:
            self.logger.info("Starting daily X bot activities")
            
            # Post to X
            post_types = ['motivational', 'business', 'engagement', 'tips']
            selected_type = random.choice(post_types)
            self.post_to_x(self.create_post_content(selected_type))
            
            # Engage with content
            search_terms = ['social media marketing', 'digital marketing', 'entrepreneurship', 'business growth']
            
            for term in search_terms[:2]:  # Limit to 2 terms per run
                self.like_posts(term, count=2)
                self.repost_content(term, count=1)
                
            self.logger.info("Completed daily X bot activities")
            
        except Exception as e:
            self.logger.error(f"Error in run_daily_activities: {e}")
            
    def get_activity_summary(self) -> Dict:
        """Get summary of X bot activities"""
        self.reset_hourly_counters()
        self.reset_daily_counters()
        
        return {
            'today': self.activity_tracker['daily_stats'],
            'this_hour': self.activity_tracker['actions_this_hour'],
            'enabled': self.enabled,
            'authenticated': self.client is not None
        }

if __name__ == "__main__":
    try:
        bot = XBot()
        print("X bot initialized successfully!")
        print("Activity summary:", bot.get_activity_summary())
        
    except Exception as e:
        print(f"Error initializing X bot: {e}")
