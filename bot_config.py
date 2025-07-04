"""
Instagram Bot Configuration
Centralized configuration for bot behavior and safety settings
"""

class BotConfig:
    """Bot configuration class"""
    
    # Instagram API Rate Limits (Conservative)
    # These are well below Instagram's limits to avoid detection
    RATE_LIMITS = {
        'likes_per_hour': 30,
        'comments_per_hour': 15,
        'follows_per_hour': 20,
        'unfollows_per_hour': 15,
        'posts_per_day': 3,
        'stories_per_day': 5
    }
    
    # Safety Delays (in seconds)
    DELAYS = {
        'min_action_delay': 30,    # Minimum delay between actions
        'max_action_delay': 120,   # Maximum delay between actions
        'login_delay': 300,        # Delay after login
        'post_delay': 600,         # Delay after posting
        'error_delay': 1800        # Delay after errors (30 minutes)
    }
    
    # Content Settings
    # Focus: Health, Wellness, Mental Health, Community, and Well-Being
    CONTENT = {
        'hashtags': [
            '#yesplease',
            '#mentalhealth',
            '#wellness',
            '#community',
            '#selfcare',
            '#mindfulness',
            '#healthyhabits',
            '#supporteachother'
        ],
        'target_hashtags': [
            'mentalhealth',
            'wellness',
            'community',
            'selfcare',
            'mindfulness',
            'healthyhabits',
            'supporteachother',
            'yesplease'
        ]
    }
    
    # Comment Templates
    COMMENTS = [
        "Great content! 🔥",
        "Love this! 💯", 
        "Amazing post! 👏",
        "Awesome! 🚀",
        "Nice work! ✨",
        "So inspiring! 💪",
        "Perfect! 🎯",
        "Incredible! 🙌",
        "Beautiful! 😍",
        "Outstanding! ⭐"
    ]
    
    # Account Safety Settings
    SAFETY = {
        'max_errors_per_hour': 5,
        'cooldown_after_errors': 3600,  # 1 hour cooldown
        'max_login_attempts': 3,
        'session_duration': 7200,       # 2 hours max session
        'daily_activity_limit': 1000    # Total daily actions
    }
    
    # Engagement Settings
    ENGAGEMENT = {
        'like_probability': 0.8,        # 80% chance to like
        'comment_probability': 0.3,     # 30% chance to comment
        'follow_probability': 0.2,      # 20% chance to follow
        'skip_business_accounts': True,
        'skip_verified_accounts': True,
        'min_followers': 100,           # Min followers to engage
        'max_followers': 100000         # Max followers to engage
    }
    
    # Schedule Settings (24-hour format)
    SCHEDULE = {
        'active_hours': {
            'start': 8,     # 8 AM
            'end': 22       # 10 PM
        },
        'post_times': ['10:00', '15:00', '19:00'],
        'engagement_times': ['09:00', '12:00', '16:00', '20:00']
    }

class SafetyChecker:
    """Safety checker to validate bot activities"""
    
    def __init__(self):
        self.error_count = 0
        self.last_error_time = None
        self.daily_actions = 0
        self.session_start = None
        
    def can_perform_action(self, action_type, current_count):
        """Check if action can be performed safely"""
        limits = BotConfig.RATE_LIMITS
        
        # Check specific action limits
        if action_type == 'like' and current_count >= limits['likes_per_hour']:
            return False, "Hourly like limit reached"
            
        if action_type == 'comment' and current_count >= limits['comments_per_hour']:
            return False, "Hourly comment limit reached"
            
        if action_type == 'follow' and current_count >= limits['follows_per_hour']:
            return False, "Hourly follow limit reached"
            
        # Check daily total actions
        if self.daily_actions >= BotConfig.SAFETY['daily_activity_limit']:
            return False, "Daily activity limit reached"
            
        # Check error rate
        if self.error_count >= BotConfig.SAFETY['max_errors_per_hour']:
            return False, "Too many errors, cooling down"
            
        return True, "OK"
        
    def record_action(self):
        """Record that an action was performed"""
        self.daily_actions += 1
        
    def record_error(self):
        """Record that an error occurred"""
        import time
        self.error_count += 1
        self.last_error_time = time.time()
        
    def should_take_break(self):
        """Check if bot should take a break"""
        import time
        
        # Take break if too many errors
        if (self.error_count >= BotConfig.SAFETY['max_errors_per_hour'] and 
            self.last_error_time and 
            time.time() - self.last_error_time < BotConfig.SAFETY['cooldown_after_errors']):
            return True, "Cooling down after errors"
            
        # Take break if session too long
        if (self.session_start and 
            time.time() - self.session_start > BotConfig.SAFETY['session_duration']):
            return True, "Session duration limit reached"
            
        return False, "OK"
        
    def reset_daily_counters(self):
        """Reset daily counters"""
        self.daily_actions = 0
        self.error_count = 0
        
    def start_session(self):
        """Start a new session"""
        import time
        self.session_start = time.time()
        
    def end_session(self):
        """End current session"""
        self.session_start = None
