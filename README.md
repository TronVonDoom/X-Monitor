# X (Twitter) Monitor 🐦

Monitor X (Twitter) accounts for new posts and get instant Pushbullet notifications. Perfect for tracking deals, announcements, or any account you want to follow closely.

## Features

- ✅ **Real-time monitoring** - Checks for new posts every 60 seconds (configurable)
- ✅ **Original posts only** - Filters out replies and retweets
- ✅ **Instant notifications** - Push alerts via Pushbullet
- ✅ **Docker-ready** - Easy deployment on Unraid or any Docker host
- ✅ **Persistent tracking** - Remembers last checked tweet across restarts
- ✅ **Rate limit friendly** - Built-in protection against API limits

## Prerequisites

### 1. Twitter/X API Credentials

You need a Twitter Developer account with API access:

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new project and app (Free tier works fine)
3. Generate your credentials:
   - API Key
   - API Key Secret
   - Bearer Token (you'll need to generate this)

**Note:** The Free tier allows 500,000 tweets read per month, which is more than enough for monitoring.

### 2. Pushbullet API Key

1. Go to [Pushbullet Settings](https://www.pushbullet.com/#settings/account)
2. Create an Access Token
3. Install Pushbullet app on your devices (iOS, Android, or browser extension)

## Quick Start

### Local Testing (Windows/Mac/Linux)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/X_Monitor.git
   cd X_Monitor
   ```

2. **Set up environment:**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env with your credentials
   # Use your favorite text editor to fill in the values
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the monitor:**
   ```bash
   python monitor.py
   ```

### Docker Deployment

#### Option 1: Docker Compose (Recommended for Unraid)

1. **Clone and configure:**
   ```bash
   git clone https://github.com/yourusername/X_Monitor.git
   cd X_Monitor
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Start the container:**
   ```bash
   docker-compose up -d
   ```

3. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

#### Option 2: Docker Run

```bash
docker build -t x-monitor .

docker run -d \
  --name x-monitor \
  --restart unless-stopped \
  -e TWITTER_API_KEY="your_key" \
  -e TWITTER_API_SECRET="your_secret" \
  -e TWITTER_BEARER_TOKEN="your_bearer_token" \
  -e PUSHBULLET_API_KEY="your_pushbullet_key" \
  -e TWITTER_USERNAME="PokemonDealsTCG" \
  -e CHECK_INTERVAL=60 \
  -v $(pwd)/data:/app/data \
  x-monitor
```

## Unraid Setup

### Using Docker Compose

1. **SSH into your Unraid server**

2. **Navigate to your appdata directory:**
   ```bash
   cd /mnt/user/appdata/
   git clone https://github.com/yourusername/X_Monitor.git
   cd X_Monitor
   ```

3. **Configure:**
   ```bash
   cp .env.example .env
   nano .env  # or use vi
   # Fill in your API credentials
   ```

4. **Start:**
   ```bash
   docker-compose up -d
   ```

### Using Unraid Docker UI

1. Go to **Docker** tab in Unraid
2. Click **Add Container**
3. Configure:
   - **Name:** x-monitor
   - **Repository:** ghcr.io/yourusername/x-monitor:latest (after you build and push)
   - **Network Type:** Bridge
   
4. Add these **Environment Variables:**
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_BEARER_TOKEN`
   - `PUSHBULLET_API_KEY`
   - `TWITTER_USERNAME` (default: PokemonDealsTCG)
   - `CHECK_INTERVAL` (default: 60)

5. Add **Path:**
   - Container Path: `/app/data`
   - Host Path: `/mnt/user/appdata/x-monitor/data`

6. Click **Apply**

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TWITTER_API_KEY` | ✅ | - | Your Twitter API Key |
| `TWITTER_API_SECRET` | ✅ | - | Your Twitter API Secret |
| `TWITTER_BEARER_TOKEN` | ✅ | - | Your Twitter Bearer Token |
| `PUSHBULLET_API_KEY` | ✅ | - | Your Pushbullet Access Token |
| `TWITTER_USERNAME` | ❌ | PokemonDealsTCG | Username to monitor (without @) |
| `CHECK_INTERVAL` | ❌ | 60 | Seconds between checks (60-300 recommended) |

### Monitoring Multiple Accounts

To monitor multiple accounts, run multiple containers with different configurations:

```bash
# Monitor PokemonDealsTCG
docker run -d --name x-monitor-pokemon \
  -e TWITTER_USERNAME="PokemonDealsTCG" \
  [other env vars...]

# Monitor another account
docker run -d --name x-monitor-other \
  -e TWITTER_USERNAME="OtherAccount" \
  [other env vars...]
```

## How It Works

1. **Initial Setup:** On first run, the monitor fetches the latest tweet to establish a baseline
2. **Continuous Monitoring:** Every `CHECK_INTERVAL` seconds, it checks for new tweets
3. **Filtering:** Automatically excludes replies and retweets (original posts only)
4. **Notifications:** Sends a Pushbullet push for each new tweet with:
   - Tweet text
   - Direct link to the tweet
5. **Persistence:** Saves the last checked tweet ID so it won't miss tweets after restarts

## Troubleshooting

### "Missing required environment variables"
- Make sure all required variables are set in your `.env` file
- Check for typos in variable names

### "User not found"
- Verify the username is correct (without @ symbol)
- Make sure the account is public

### "Rate limit exceeded"
- Increase `CHECK_INTERVAL` to check less frequently
- Twitter's free tier has generous limits, but aggressive checking can hit them

### No notifications received
- Check Pushbullet app is installed and logged in
- Verify your Pushbullet API key is correct
- Check the logs: `docker-compose logs -f`

### Container keeps restarting
- Check logs: `docker logs x-monitor`
- Verify all environment variables are set correctly
- Ensure the Twitter API credentials are valid

## Logs

Logs are written to:
- Console output (visible with `docker logs`)
- `monitor.log` file in the container

To view logs:
```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f x-monitor

# Local
tail -f monitor.log
```

## Updating

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## Security Notes

- ⚠️ **Never commit your `.env` file** - It's in `.gitignore` for safety
- ⚠️ **Never share your API keys** - Treat them like passwords
- ⚠️ **Regenerate keys if exposed** - Better safe than sorry
- ✅ **Use environment variables** - Don't hardcode credentials

## GitHub Setup

Before pushing to GitHub:

1. **Verify `.env` is ignored:**
   ```bash
   git status
   # .env should NOT appear in the list
   ```

2. **Only commit these files:**
   - `monitor.py`
   - `requirements.txt`
   - `Dockerfile`
   - `docker-compose.yml`
   - `.env.example`
   - `.gitignore`
   - `README.md`

3. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/X_Monitor.git
   git push -u origin main
   ```

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Issues and pull requests are welcome!

## Support

If you find this useful, consider:
- ⭐ Starring the repo
- 🐛 Reporting bugs
- 💡 Suggesting features

---

**Made with ❤️ for tracking Pokemon TCG deals (or whatever you want to monitor!)**
