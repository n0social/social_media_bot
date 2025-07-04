# YesPlease Social Media Bot

A sophisticated social media automation bot designed to help grow your "Yes Please" brand on **Instagram** and **X (formerly Twitter)** while staying within platform guidelines and avoiding bans.

## Features

- **Multi-Platform Support**: Automate both Instagram and X (Twitter) from one system
- **Automated Posting**: Schedule and post content automatically to both platforms
- **Smart Engagement**: Like, comment, follow, and repost content based on hashtags
- **Cross-Platform Posting**: Post the same content to multiple platforms with delays
- **Rate Limiting**: Built-in safety measures to avoid platform spam detection
- **Activity Tracking**: Monitor daily activities and limits across all platforms
- **Content Management**: Easy content upload and management for multiple platforms
- **Unified Dashboard**: Manage all platforms from one interactive interface
- **Comprehensive Logging**: Platform-specific logging for monitoring and debugging

## Supported Platforms

### 📷 Instagram
- Automated posting of images and videos
- Like, comment, and follow users based on hashtags
- Story posting support
- Advanced engagement algorithms

### 🐦 X (formerly Twitter)
- Automated posting of text and media
- Like, repost, and follow users based on keywords
- Thread support
- Trending hashtag integration

## Safety Features

- **Daily Limits**: Configurable limits for all actions across platforms
- **Random Delays**: Human-like delays between actions (30-120 seconds)
- **Cross-Platform Coordination**: Intelligent scheduling to avoid conflicts
- **Activity Tracking**: Prevents exceeding daily limits on any platform
- **Error Handling**: Robust error handling and recovery
- **Platform-Specific Rate Limits**: Respects each platform's unique limitations

## Installation

1. **Clone/Download the project**
   ```bash
   cd YesPlease_SocialMedia
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Edit `.env` file and fill in your credentials for both platforms
   - Adjust bot settings as needed

4. **Add content to post**
   - Place your images/videos in the `content/` folder
   - Supported formats: JPG, PNG, MP4

## Configuration

Edit the `.env` file with your settings:

```env
# Instagram Credentials
INSTAGRAM_USERNAME=your_username_here
INSTAGRAM_PASSWORD=your_password_here

# X (Twitter) API Credentials
X_API_KEY=your_x_api_key_here
X_API_SECRET=your_x_api_secret_here
X_ACCESS_TOKEN=your_x_access_token_here
X_ACCESS_TOKEN_SECRET=your_x_access_token_secret_here
X_BEARER_TOKEN=your_x_bearer_token_here

# Platform Settings
ENABLE_INSTAGRAM=true
ENABLE_X=true
ENABLE_CROSS_POSTING=true

# Bot Limits (per day)
MAX_LIKES_PER_HOUR=30
MAX_COMMENTS_PER_HOUR=15
MAX_FOLLOWS_PER_HOUR=20
MAX_POSTS_PER_DAY=10
MAX_REPOSTS_PER_HOUR=20

# Content
CONTENT_FOLDER=content
HASHTAGS=#yesplease #socialmedia #content
X_HASHTAGS=#YesPlease #SocialMedia #Content #X #Business

# Safety
ENABLE_SAFETY_DELAYS=true
MIN_ACTION_DELAY=30
MAX_ACTION_DELAY=120
```

## Getting X (Twitter) API Access

To use the X bot, you need to get API access:

1. **Apply for Developer Account**: Visit [developer.x.com](https://developer.x.com)
2. **Create a New App**: Set up your application
3. **Generate API Keys**: Get your API keys and tokens
4. **Add to .env**: Update your `.env` file with the credentials

### Required X API Permissions:
- Read and Write posts
- Engage with posts (like, repost)
- Manage followers

## Usage

### Option 1: Interactive Manager (Recommended)
```bash
python bot_manager.py
```

This launches an interactive menu where you can:
- Run unified bot (both platforms)
- Run individual platform bots
- Start scheduled automation
- Check activity logs across platforms
- Test platform connections
- View bot configuration

### Option 2: Windows Batch File
```bash
run_bot.bat
```

### Option 3: Direct Script Execution
```bash
# Unified bot
python social_media_bot.py

# Instagram only
python instagram_bot.py

# X only  
python x_bot.py
```

## How It Works

### Daily Schedule
The bot runs 4 times per day across platforms:
- 9:00 AM - Full posting and engagement
- 1:00 PM - Full posting and engagement  
- 5:00 PM - Full posting and engagement
- 8:00 PM - Full posting and engagement

### Additional Engagement Activities
- 11:00 AM - Instagram engagement only
- 3:00 PM - X engagement only
- 7:00 PM - Instagram engagement only

### Cross-Platform Coordination
- **Intelligent Delays**: 1-3 minutes between platform posts
- **Content Adaptation**: Platform-specific formatting
- **Hashtag Optimization**: Different hashtag strategies per platform
- **Engagement Balancing**: Distributes activities across platforms

## Content Management

### Adding Content
1. Place your images/videos in the `content/` folder
2. Supported formats: `.jpg`, `.jpeg`, `.png`, `.mp4`
3. The bot will automatically select random content to post

### Content Tips
- Use high-quality images (1080x1080 recommended)
- Keep videos under 60 seconds
- Name files descriptively for logging purposes

## Monitoring

### Activity Logs
- Check `instagram_bot.log` for detailed activity logs
- View `activity_log.json` for current statistics
- Use the bot manager to check status interactively

### Key Metrics Tracked
- Daily likes, comments, follows
- Last post timestamp
- Error occurrences
- Login attempts

## Instagram Limits & Safety

### Recommended Daily Limits
- **Likes**: 480 per day (30/hour × 16 hours)
- **Comments**: 240 per day (15/hour × 16 hours)
- **Follows**: 320 per day (20/hour × 16 hours)
- **Posts**: 1-3 per day maximum

### Safety Best Practices
- Start with lower limits and gradually increase
- Monitor your account for any warnings
- Use authentic, relevant hashtags
- Avoid aggressive following/unfollowing
- Don't run 24/7 - take breaks

## Troubleshooting

### Common Issues

**Login Failures**
- Check username/password in `.env`
- Instagram may require 2FA - disable temporarily
- Try logging in manually first

**Rate Limit Errors**
- Reduce limits in `.env`
- Increase delay intervals
- Check if account is temporarily restricted

**Content Not Posting**
- Verify content folder exists and has files
- Check file formats are supported
- Ensure images are valid and not corrupted

### Error Logs
Check `instagram_bot.log` for detailed error information:
```bash
# Windows
type instagram_bot.log

# View last 50 lines
Get-Content instagram_bot.log -Tail 50
```

## Important Disclaimers

⚠️ **Use at Your Own Risk**: Instagram automation violates Instagram's Terms of Service. Use this bot responsibly and at your own risk.

⚠️ **Account Safety**: Start with conservative settings and monitor your account closely. Instagram can suspend accounts for automation.

⚠️ **Compliance**: Ensure your content and engagement practices comply with Instagram's community guidelines.

## Support

For issues or questions:
1. Check the logs first
2. Review Instagram's current policies
3. Adjust settings conservatively
4. Test with a secondary account first

## License

This project is for educational purposes. Use responsibly and in compliance with Instagram's Terms of Service.
