#!/usr/bin/env python3
"""
X (Twitter) Monitor - Track new posts from specific users
Monitors PokemonDealsTCG for new posts and sends Pushbullet notifications
"""

import os
import time
import tweepy
from pushbullet import Pushbullet
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables early so LOG_FILE or CHECK_INTERVAL can be honored
load_dotenv()

# Logging: write to a persisted file inside /app/data to avoid host path conflicts
LOG_FILE = os.getenv('LOG_FILE', '/app/data/monitor.log')
try:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
except Exception:
    # Best-effort; if this fails the FileHandler may still create the file in container FS
    pass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
PUSHBULLET_API_KEY = os.getenv('PUSHBULLET_API_KEY')
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME', 'PokemonDealsTCG')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 60))  # seconds
LAST_TWEET_FILE = 'last_tweet_id.txt'


def get_twitter_client():
    """Initialize and return Twitter API client"""
    try:
        client = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            wait_on_rate_limit=True
        )
        logger.info("Twitter API client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Twitter client: {e}")
        raise


def get_pushbullet_client():
    """Initialize and return Pushbullet client"""
    try:
        pb = Pushbullet(PUSHBULLET_API_KEY)
        logger.info("Pushbullet client initialized successfully")
        return pb
    except Exception as e:
        logger.error(f"Failed to initialize Pushbullet client: {e}")
        raise


def load_last_tweet_id():
    """Load the last processed tweet ID from file"""
    try:
        if os.path.exists(LAST_TWEET_FILE):
            with open(LAST_TWEET_FILE, 'r') as f:
                tweet_id = f.read().strip()
                if tweet_id:
                    logger.info(f"Loaded last tweet ID: {tweet_id}")
                    return tweet_id
    except Exception as e:
        logger.warning(f"Could not load last tweet ID: {e}")
    return None


def save_last_tweet_id(tweet_id):
    """Save the last processed tweet ID to file"""
    try:
        with open(LAST_TWEET_FILE, 'w') as f:
            f.write(str(tweet_id))
        logger.debug(f"Saved last tweet ID: {tweet_id}")
    except Exception as e:
        logger.error(f"Failed to save last tweet ID: {e}")


def get_user_id(client, username):
    """Get user ID from username"""
    try:
        user = client.get_user(username=username)
        if user.data:
            logger.info(f"Found user {username} with ID: {user.data.id}")
            return user.data.id
        else:
            logger.error(f"User {username} not found")
            return None
    except Exception as e:
        logger.error(f"Error getting user ID for {username}: {e}")
        return None


def check_new_tweets(client, user_id, since_id=None):
    """
    Check for new tweets from the user
    Only returns original posts (excludes replies and retweets)
    """
    try:
        # Get user's tweets
        # exclude='retweets,replies' ensures we only get original posts
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=10,
            since_id=since_id,
            exclude=['retweets', 'replies'],
            tweet_fields=['created_at', 'text', 'id']
        )
        
        if tweets.data:
            logger.info(f"Found {len(tweets.data)} new tweet(s)")
            return tweets.data
        else:
            logger.debug("No new tweets found")
            return []
            
    except Exception as e:
        logger.error(f"Error checking tweets: {e}")
        return []


def send_pushbullet_notification(pb, tweet, username):
    """Send a Pushbullet notification for a new tweet"""
    try:
        tweet_url = f"https://twitter.com/{username}/status/{tweet.id}"
        title = f"🐦 New post from @{username}"
        
        # Format the message
        message = f"{tweet.text}\n\n🔗 {tweet_url}"
        
        # Send push notification
        push = pb.push_link(title, tweet_url, body=tweet.text)
        logger.info(f"Sent Pushbullet notification for tweet {tweet.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send Pushbullet notification: {e}")
        return False


def monitor_loop():
    """Main monitoring loop"""
    logger.info("=" * 50)
    logger.info("X Monitor Starting")
    logger.info(f"Monitoring: @{TWITTER_USERNAME}")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
    logger.info("=" * 50)
    
    # Initialize clients
    twitter_client = get_twitter_client()
    pushbullet_client = get_pushbullet_client()
    
    # Get user ID
    user_id = get_user_id(twitter_client, TWITTER_USERNAME)
    if not user_id:
        logger.error("Cannot continue without user ID")
        return
    
    # Load last tweet ID
    last_tweet_id = load_last_tweet_id()
    
    # If no last tweet ID, get the most recent tweet to start monitoring from
    if not last_tweet_id:
        logger.info("No previous tweet ID found, fetching latest tweet to establish baseline...")
        initial_tweets = check_new_tweets(twitter_client, user_id)
        if initial_tweets:
            last_tweet_id = initial_tweets[0].id
            save_last_tweet_id(last_tweet_id)
            logger.info(f"Baseline established with tweet ID: {last_tweet_id}")
            logger.info("Will monitor for new tweets from this point forward")
    
    logger.info("Monitoring active - Press Ctrl+C to stop")
    
    # Main monitoring loop
    try:
        while True:
            new_tweets = check_new_tweets(twitter_client, user_id, last_tweet_id)
            
            # Process new tweets (oldest first)
            if new_tweets:
                # Sort by ID (oldest first) to maintain chronological order
                new_tweets.sort(key=lambda x: x.id)
                
                for tweet in new_tweets:
                    logger.info(f"New tweet detected: {tweet.text[:50]}...")
                    send_pushbullet_notification(pushbullet_client, tweet, TWITTER_USERNAME)
                    
                    # Update last tweet ID
                    last_tweet_id = tweet.id
                    save_last_tweet_id(last_tweet_id)
            
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("\nMonitoring stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error in monitoring loop: {e}")
        raise


if __name__ == "__main__":
    # Validate environment variables
    required_vars = {
        'TWITTER_API_KEY': TWITTER_API_KEY,
        'TWITTER_API_SECRET': TWITTER_API_SECRET,
        'TWITTER_BEARER_TOKEN': TWITTER_BEARER_TOKEN,
        'PUSHBULLET_API_KEY': PUSHBULLET_API_KEY
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check your .env file")
        exit(1)
    
    # Start monitoring
    monitor_loop()
