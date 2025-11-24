# X.com (Twitter) Monitor with Pushbullet Notifications

This Docker container monitors @PokemonDealsTCG on X.com (formerly Twitter) and sends instant push notifications to your Android phone via Pushbullet whenever they post a new tweet.

## 📋 Prerequisites

1. **Pushbullet Account & API Token** ✅ (Already configured)
   - You have: `o.dzHSKHotDMwB5h0uYEOoYgPbkGfkOr0b`

2. **X/Twitter Bearer Token** ✅ (Already configured)
   - You have: `AAAAAAAAAAAAAAAAAAAAAJ9v5gEAAAAACSFXftx3lg7t6DvanMulArumd1k...`

3. **Pushbullet App on Android**
   - Download from Google Play Store
   - Sign in with your Pushbullet account

## 🚀 Installation on Unraid

### Method 1: Using Unraid Docker UI (Easiest)

1. **Upload Files to Unraid**
   - Copy the entire `X_Monitor` folder to your Unraid server
   - Suggested location: `/mnt/user/appdata/x-monitor/`
   - You can use the Unraid web interface, WinSCP, or SMB to transfer files

2. **Open Unraid Docker Tab**
   - Go to your Unraid web interface
   - Click on the **Docker** tab

3. **Add Container**
   - Click **"Add Container"** at the bottom
   - Fill in the following:

   **Container Settings:**
   - **Name:** `x-monitor`
   - **Repository:** `python:3.11-slim`
   - **Network Type:** `Bridge`
   - **Console shell command:** `Bash`

   **Environment Variables (Click "Add another Path, Port, Variable, Label or Device"):**
   - Variable: `PUSHBULLET_TOKEN` | Value: `o.dzHSKHotDMwB5h0uYEOoYgPbkGfkOr0b`
   - Variable: `TWITTER_BEARER_TOKEN` | Value: `AAAAAAAAAAAAAAAAAAAAAJ9v5gEAAAAACSFXftx3lg7t6DvanMulArumd1k%3DXBCUZG1guQEL5mfuHUwCrlvDIgAJDu9kHLDhqpVJUnqtTPhiAj`
   - Variable: `TWITTER_USERNAME` | Value: `PokemonDealsTCG`
   - Variable: `CHECK_INTERVAL` | Value: `60`

   **Paths:**
   - Container Path: `/app` | Host Path: `/mnt/user/appdata/x-monitor` | Access Mode: `Read/Write`
   - Container Path: `/app/data` | Host Path: `/mnt/user/appdata/x-monitor/data` | Access Mode: `Read/Write`

   **Post Arguments (Important!):**
   ```
   bash -c "pip install requests && python -u /app/x_monitor.py"
   ```

4. **Apply and Start**
   - Click **"Apply"**
   - The container will start automatically

---

### Method 2: Using Docker Compose (Recommended for Advanced Users)

1. **SSH into your Unraid server**

2. **Create the directory and navigate to it:**
   ```bash
   mkdir -p /mnt/user/appdata/x-monitor
   cd /mnt/user/appdata/x-monitor
   ```

3. **Upload all files from the `X_Monitor` folder to this directory**
   - `Dockerfile`
   - `docker-compose.yml`
   - `x_monitor.py`
   - `config.env`

4. **Create the data directory:**
   ```bash
   mkdir -p data
   ```

5. **Build and start the container:**
   ```bash
   docker-compose up -d --build
   ```

6. **View logs to confirm it's working:**
   ```bash
   docker-compose logs -f
   ```

---

## 📱 How It Works

1. **Every 60 seconds**, the script checks @PokemonDealsTCG for new tweets
2. **When a new tweet is detected**, it sends a Pushbullet notification to your Android phone
3. **You get an instant notification** with the tweet text and a direct link
4. **State persistence**: The last tweet ID is saved so you don't get duplicate notifications

---

## 🔧 Configuration

Edit `config.env` to change settings:

- **TWITTER_USERNAME**: Account to monitor (default: `PokemonDealsTCG`)
- **CHECK_INTERVAL**: How often to check in seconds (default: `60`)
- **PUSHBULLET_TOKEN**: Your Pushbullet API token
- **TWITTER_BEARER_TOKEN**: Your Twitter API Bearer token

---

## 📊 Monitoring & Troubleshooting

### View Container Logs

**Via Unraid UI:**
- Go to Docker tab → Click the container → Click "Logs"

**Via Command Line:**
```bash
docker logs -f x-monitor
```

### Check if Container is Running
```bash
docker ps | grep x-monitor
```

### Restart Container
```bash
docker restart x-monitor
```

### Stop Container
```bash
docker stop x-monitor
```

---

## ✅ Testing

1. **Start the container**
2. **You should receive a test notification** on your phone: "✅ X Monitor Started"
3. **Wait for @PokemonDealsTCG to post** (or manually trigger a test by deleting `/mnt/user/appdata/x-monitor/data/last_tweet_id.json` and restarting)

---

## 🛡️ Security Notes

- Your `config.env` contains sensitive API tokens
- Keep this file secure and don't share it
- The tokens are stored only on your Unraid server
- Consider changing permissions: `chmod 600 config.env`

---

## 🔄 Updates

To update the script:
1. Edit `x_monitor.py` with your changes
2. Restart the container:
   ```bash
   docker restart x-monitor
   ```

---

## ❓ FAQ

**Q: How do I change the check interval?**  
A: Edit `CHECK_INTERVAL` in `config.env` (in seconds), then restart the container.

**Q: Can I monitor multiple accounts?**  
A: Currently, it monitors one account. You'd need to run multiple containers with different configs.

**Q: I'm not getting notifications on my phone?**  
A: Check:
- Pushbullet app is installed and logged in
- Container logs show "✅ Notification sent"
- Your Pushbullet token is correct
- Phone notifications are enabled for Pushbullet

**Q: Does this use a lot of resources?**  
A: No, it's very lightweight. Uses ~50MB RAM and minimal CPU.

---

## 📞 Support

Check the logs first if something isn't working:
```bash
docker logs x-monitor
```

Common log messages:
- `✅ Notification sent` - Working correctly
- `❌ Error fetching tweets` - Twitter API issue
- `❌ Pushbullet error` - Pushbullet API issue
- `📬 Found X new tweet(s)` - New tweets detected
- `✔️ No new tweets` - Monitoring but nothing new

---

**Created:** November 2025  
**Monitoring:** @PokemonDealsTCG  
**Platform:** Unraid Docker
