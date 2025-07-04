import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import available bots
try:
    from instagram_bot import InstagramBot
    INSTAGRAM_AVAILABLE = True
except ImportError:
    INSTAGRAM_AVAILABLE = False

try:
    from x_bot import XBot
    X_AVAILABLE = True
except ImportError:
    X_AVAILABLE = False

try:
    from social_media_bot import SocialMediaBot
    UNIFIED_BOT_AVAILABLE = True
except ImportError:
    UNIFIED_BOT_AVAILABLE = False

def main():
    """Main function to run the social media bot manager"""
    print("🚀 YesPlease Social Media Bot Manager")
    print("=" * 50)
    
    # Show available platforms
    platforms = []
    if INSTAGRAM_AVAILABLE:
        platforms.append("Instagram")
    if X_AVAILABLE:
        platforms.append("X")
    
    print(f"Available platforms: {', '.join(platforms) if platforms else 'None'}")
    print()
    
    while True:
        print("\nAvailable options:")
        print("1. Run unified bot (Instagram + X)")
        print("2. Run Instagram bot only")
        print("3. Run X bot only")
        print("4. Start scheduled automation")
        print("5. Check activity logs")
        print("6. Test connections")
        print("7. Bot configuration")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            run_unified_bot()
        elif choice == '2':
            run_instagram_bot()
        elif choice == '3':
            run_x_bot()
        elif choice == '4':
            start_scheduled_bot()
        elif choice == '5':
            check_activity_logs()
        elif choice == '6':
            test_connections()
        elif choice == '7':
            show_configuration()
        elif choice == '8':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please try again.")

def run_unified_bot():
    """Run the unified social media bot"""
    if not UNIFIED_BOT_AVAILABLE:
        print("❌ Unified bot not available")
        return
        
    print("\n🚀 Running unified social media bot...")
    try:
        bot = SocialMediaBot()
        bot.run_daily_activities()
        print("✅ Unified bot run completed successfully!")
        
        # Show summary
        summary = bot.get_unified_summary()
        print(f"\n📊 Results summary:")
        print(f"Active platforms: {summary['platforms_active']}")
        if summary.get('daily_stats'):
            for activity, count in summary['daily_stats'].items():
                print(f"- {activity}: {count}")
                
    except Exception as e:
        print(f"❌ Error running unified bot: {e}")

def run_instagram_bot():
    """Run Instagram bot and keep it running with the scheduler"""
    if not INSTAGRAM_AVAILABLE:
        print("❌ Instagram bot not available")
        return
        
    print("\n📷 Starting Instagram bot scheduler (continuous posting)...")
    try:
        bot = InstagramBot()
        bot.start_scheduler()
    except Exception as e:
        print(f"❌ Error running Instagram bot: {e}")

def run_x_bot():
    """Run X bot only"""
    if not X_AVAILABLE:
        print("❌ X bot not available")
        return
        
    print("\n🐦 Running X bot...")
    try:
        bot = XBot()
        bot.run_daily_activities()
        print("✅ X bot run completed successfully!")
    except Exception as e:
        print(f"❌ Error running X bot: {e}")

def start_scheduled_bot():
    """Start the scheduled bot"""
    print("\n⏰ Starting scheduled social media bot...")
    print("The bot will run automatically at scheduled times.")
    print("Press Ctrl+C to stop the bot.")
    
    try:
        if UNIFIED_BOT_AVAILABLE:
            print("Using unified social media bot for scheduling")
            bot = SocialMediaBot()
        elif INSTAGRAM_AVAILABLE:
            print("Using Instagram bot for scheduling")
            bot = InstagramBot()
        else:
            print("❌ No bots available for scheduling")
            return
            
        bot.start_scheduler()
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running scheduled bot: {e}")

def check_activity_logs():
    """Check activity logs for all platforms"""
    print("\n📊 Activity Logs:")
    print("-" * 40)
    
    # Check unified activity
    try:
        unified_file = Path('data/social_media_activity.json')
        if unified_file.exists():
            import json
            with open(unified_file, 'r') as f:
                data = json.load(f)
            
            print("🔄 Unified Bot Activity:")
            print(f"  Session start: {data.get('session_start', 'N/A')}")
            print(f"  Platforms active: {data.get('platforms_active', [])}")
            if data.get('daily_stats'):
                print("  Daily stats:")
                for activity, count in data['daily_stats'].items():
                    print(f"    {activity}: {count}")
            print()
    except Exception as e:
        print(f"❌ Error reading unified activity: {e}")
    
    # Check Instagram activity
    try:
        instagram_file = Path('activity_log.json')
        if instagram_file.exists():
            import json
            with open(instagram_file, 'r') as f:
                data = json.load(f)
                
            print("📷 Instagram Activity:")
            print(f"  Likes today: {data.get('likes_today', 0)}")
            print(f"  Comments today: {data.get('comments_today', 0)}")
            print(f"  Follows today: {data.get('follows_today', 0)}")
            print(f"  Last post: {data.get('last_post', 'N/A')}")
            print()
    except Exception as e:
        print(f"❌ Error reading Instagram activity: {e}")
    
    # Check X activity
    try:
        x_file = Path('data/x_activity.json')
        if x_file.exists():
            import json
            with open(x_file, 'r') as f:
                data = json.load(f)
                
            print("🐦 X Activity:")
            if data.get('daily_stats'):
                for activity, count in data['daily_stats'].items():
                    print(f"  {activity}: {count}")
            print(f"  Last reset: {data.get('last_activity_reset', 'N/A')}")
            print()
    except Exception as e:
        print(f"❌ Error reading X activity: {e}")

def test_connections():
    """Test connections to all platforms"""
    print("\n🔗 Testing Platform Connections:")
    print("-" * 40)
    
    # Test Instagram
    if INSTAGRAM_AVAILABLE:
        print("� Testing Instagram connection...")
        try:
            bot = InstagramBot()
            if bot.login():
                print("✅ Instagram connection successful!")
                try:
                    bot.client.logout()
                except:
                    pass
            else:
                print("❌ Instagram connection failed")
        except Exception as e:
            print(f"❌ Instagram connection error: {e}")
    else:
        print("⚠️  Instagram bot not available")
    
    print()
    
    # Test X
    if X_AVAILABLE:
        print("🐦 Testing X connection...")
        try:
            bot = XBot()
            if bot.client:
                print("✅ X connection successful!")
            else:
                print("❌ X connection failed")
        except Exception as e:
            print(f"❌ X connection error: {e}")
    else:
        print("⚠️  X bot not available")

def show_configuration():
    """Show current bot configuration"""
    print("\n⚙️  Bot Configuration:")
    print("-" * 40)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Platform status
    print("🔧 Platform Status:")
    instagram_enabled = os.getenv('ENABLE_INSTAGRAM', 'true').lower() == 'true'
    x_enabled = os.getenv('ENABLE_X', 'true').lower() == 'true'
    
    print(f"  Instagram: {'✅ Enabled' if instagram_enabled else '❌ Disabled'}")
    print(f"  X: {'✅ Enabled' if x_enabled else '❌ Disabled'}")
    print()
    
    # Rate limits
    print("📊 Rate Limits:")
    print(f"  Max likes per hour: {os.getenv('MAX_LIKES_PER_HOUR', 30)}")
    print(f"  Max comments per hour: {os.getenv('MAX_COMMENTS_PER_HOUR', 15)}")
    print(f"  Max follows per hour: {os.getenv('MAX_FOLLOWS_PER_HOUR', 20)}")
    print(f"  Max posts per day: {os.getenv('MAX_POSTS_PER_DAY', 10)}")
    print()
    
    # Content settings
    print("📁 Content Settings:")
    content_folder = os.getenv('CONTENT_FOLDER', 'content')
    print(f"  Content folder: {content_folder}")
    
    # Count content files
    content_path = Path(content_folder)
    if content_path.exists():
        content_files = list(content_path.glob('*.jpg')) + list(content_path.glob('*.png')) + list(content_path.glob('*.mp4'))
        print(f"  Content files: {len(content_files)}")
    else:
        print("  Content files: 0 (folder not found)")
    
    print(f"  Instagram hashtags: {os.getenv('HASHTAGS', 'Not set')}")
    print(f"  X hashtags: {os.getenv('X_HASHTAGS', 'Not set')}")
    print()
    
    # Safety settings
    print("🛡️  Safety Settings:")
    cross_posting = os.getenv('ENABLE_CROSS_POSTING', 'true').lower() == 'true'
    print(f"  Cross-posting: {'✅ Enabled' if cross_posting else '❌ Disabled'}")
    print(f"  Post interval: {os.getenv('POST_INTERVAL_HOURS', 24)} hours")

if __name__ == "__main__":
    main()
