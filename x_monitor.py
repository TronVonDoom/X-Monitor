#!/usr/bin/env python3
"""
X.com (Twitter) Monitor with Pushbullet Notifications
Monitors @PokemonDealsTCG for new tweets and sends instant notifications
"""

import os
import json
import time
import requests
from datetime import datetime

# Configuration
PUSHBULLET_TOKEN = os.getenv('PUSHBULLET_TOKEN')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME', 'PokemonDealsTCG')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '60'))  # seconds
STATE_FILE = '/app/data/last_tweet_id.json'

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}", flush=True)

def send_pushbullet_notification(title, body, url=None):
    """Send a push notification via Pushbullet"""
    try:
        headers = {
            'Access-Token': PUSHBULLET_TOKEN,
            'Content-Type': 'application/json'
        }
        
        data = {
            'type': 'note',
            'title': title,
            'body': body
        }
        
        if url:
            data['type'] = 'link'
            data['url'] = url
        
        response = requests.post(
            'https://api.pushbullet.com/v2/pushes',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            log(f"✅ Notification sent: {title}")
            return True
        else:
            log(f"❌ Pushbullet error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        log(f"❌ Error sending notification: {e}")
        return False

def get_user_tweets(username):
    """Fetch recent tweets from a user using Twitter API v2"""
    try:
        # First, get the user ID from username
        user_url = f"https://api.twitter.com/2/users/by/username/{username}"
        headers = {
            'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'
        }
        
        user_response = requests.get(user_url, headers=headers)
        
        if user_response.status_code != 200:
            log(f"❌ Error fetching user ID: {user_response.status_code} - {user_response.text}")
            return None
        
        user_id = user_response.json()['data']['id']
        
        # Now get the user's tweets
        tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        params = {
            'max_results': 5,
            'tweet.fields': 'created_at,text',
            'exclude': 'retweets'
        }
        
        tweets_response = requests.get(tweets_url, headers=headers, params=params)
        
        if tweets_response.status_code == 200:
            return tweets_response.json()
        else:
            log(f"❌ Error fetching tweets: {tweets_response.status_code} - {tweets_response.text}")
            return None
            
    except Exception as e:
        log(f"❌ Error fetching tweets: {e}")
        return None

def load_last_tweet_id():
    """Load the last processed tweet ID from file"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('last_tweet_id')
    except Exception as e:
        log(f"⚠️ Could not load state file: {e}")
    return None

def save_last_tweet_id(tweet_id):
    """Save the last processed tweet ID to file"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump({'last_tweet_id': tweet_id}, f)
    except Exception as e:
        log(f"⚠️ Could not save state file: {e}")

def check_for_new_tweets():
    """Check for new tweets and send notifications"""
    tweets_data = get_user_tweets(TWITTER_USERNAME)
    
    if not tweets_data or 'data' not in tweets_data:
        return
    
    tweets = tweets_data['data']
    last_tweet_id = load_last_tweet_id()
    
    # If this is the first run, just save the latest tweet ID
    if last_tweet_id is None:
        if tweets:
            save_last_tweet_id(tweets[0]['id'])
            log(f"📝 Initialized with latest tweet ID: {tweets[0]['id']}")
        return
    
    # Check for new tweets (they come newest first)
    new_tweets = []
    for tweet in tweets:
        if int(tweet['id']) > int(last_tweet_id):
            new_tweets.append(tweet)
        else:
            break
    
    # Send notifications for new tweets (oldest first)
    if new_tweets:
        new_tweets.reverse()  # Show oldest new tweet first
        for tweet in new_tweets:
            tweet_url = f"https://twitter.com/{TWITTER_USERNAME}/status/{tweet['id']}"
            title = f"🔔 New tweet from @{TWITTER_USERNAME}!"
            body = tweet['text'][:200]  # Limit to 200 chars
            
            send_pushbullet_notification(title, body, tweet_url)
            save_last_tweet_id(tweet['id'])
            
        log(f"📬 Found {len(new_tweets)} new tweet(s)")
    else:
        log(f"✔️ No new tweets")

def main():
    """Main monitoring loop"""
    log("=" * 60)
    log("🚀 X.com Monitor Starting...")
    log(f"👤 Monitoring: @{TWITTER_USERNAME}")
    log(f"⏱️ Check interval: {CHECK_INTERVAL} seconds")
    log("=" * 60)
    
    # Validate configuration
    if not PUSHBULLET_TOKEN:
        log("❌ ERROR: PUSHBULLET_TOKEN not set!")
        return
    
    if not TWITTER_BEARER_TOKEN:
        log("❌ ERROR: TWITTER_BEARER_TOKEN not set!")
        return
    
    # Send test notification
    send_pushbullet_notification(
        "✅ X Monitor Started",
        f"Now monitoring @{TWITTER_USERNAME} for new tweets!"
    )
    
    # Main loop
    while True:
        try:
            check_for_new_tweets()
        except Exception as e:
            log(f"❌ Error in main loop: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
