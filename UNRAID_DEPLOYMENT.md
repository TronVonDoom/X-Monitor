# Unraid Deployment Guide

## Step 1: Push to GitHub (Do this on your Windows PC)

```powershell
# Navigate to your project
cd C:\Users\TronVonDoom\Documents\GitHub\X_Monitor

# Initialize git (if not already done)
git init

# Add all files (except .env which is ignored)
git add .

# Commit
git commit -m "X Monitor - Track PokemonDealsTCG posts with Pushbullet"

# Add your GitHub remote (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/X_Monitor.git

# Push to GitHub
git push -u origin main
```

**⚠️ IMPORTANT:** Your `.env` file with real API keys will NOT be pushed (it's in `.gitignore`). Only `.env.example` goes to GitHub.

---

## Step 2: Deploy to Unraid

### Option A: Using Unraid Terminal (Recommended - Easiest)

1. **Open Unraid Web UI** and go to the Terminal (or SSH into your server)

2. **Navigate to appdata:**
   ```bash
   cd /mnt/user/appdata/
   ```

3. **Clone your repository:**
   ```bash
   # Replace 'yourusername' with your actual GitHub username
   git clone https://github.com/yourusername/X_Monitor.git
   cd X_Monitor
   ```

4. **Create your .env file with real credentials:**
   ```bash
   nano .env
   ```
   
   Paste this (with your actual values):
   ```
   TWITTER_API_KEY=W7Hpb5n8mu37h13b7bZzDHtab
   TWITTER_API_SECRET=0DX5IMbnKkHEbwoNVh3zqJGtGedVxspTfndjJYxqWMgPNm1YFC
   TWITTER_BEARER_TOKEN=your_bearer_token_here
   PUSHBULLET_API_KEY=o.RoQCInckwsvpggwANjF6EQ8Gu7vVNE4J
   TWITTER_USERNAME=PokemonDealsTCG
   CHECK_INTERVAL=60
   ```
   
   Press `Ctrl+X`, then `Y`, then `Enter` to save.

5. **Create data directory:**
   ```bash
   mkdir -p data
   ```

6. **Start the container:**
   ```bash
   docker-compose up -d
   ```

7. **Check it's running:**
   ```bash
   docker-compose logs -f
   ```
   
   You should see:
   - "Twitter API client initialized successfully"
   - "Pushbullet client initialized successfully"
   - "Monitoring active - Press Ctrl+C to stop"
   
   Press `Ctrl+C` to exit logs (container keeps running)

8. **Check status anytime:**
   ```bash
   cd /mnt/user/appdata/X_Monitor
   docker-compose logs -f
   ```

---

### Option B: Using Unraid Docker UI (Manual Setup)

1. **Go to Docker tab** in Unraid Web UI

2. **Click "Add Container"**

3. **Fill in these settings:**

   **Basic Settings:**
   - Name: `x-monitor`
   - Repository: `python:3.11-slim`
   - Network Type: `Bridge`
   - Console shell command: `Bash`

   **Environment Variables** (click "Add another Path, Port, Variable, Label or Device"):
   
   | Key | Value |
   |-----|-------|
   | `TWITTER_API_KEY` | `W7Hpb5n8mu37h13b7bZzDHtab` |
   | `TWITTER_API_SECRET` | `0DX5IMbnKkHEbwoNVh3zqJGtGedVxspTfndjJYxqWMgPNm1YFC` |
   | `TWITTER_BEARER_TOKEN` | `your_bearer_token_here` |
   | `PUSHBULLET_API_KEY` | `o.RoQCInckwsvpggwANjF6EQ8Gu7vVNE4J` |
   | `TWITTER_USERNAME` | `PokemonDealsTCG` |
   | `CHECK_INTERVAL` | `60` |

   **Paths:**
   - Container Path: `/app/data`
   - Host Path: `/mnt/user/appdata/x-monitor/data`
   - Access Mode: Read/Write

   **Advanced:**
   - Restart Policy: `unless-stopped`
   - Post Arguments: Leave empty for now (we'll set this up differently)

4. **Click Apply**

⚠️ **Note:** Option B requires more manual setup. Option A with docker-compose is much easier!

---

## Step 3: Verify It's Working

### Test Pushbullet:
You should receive a Pushbullet notification the next time PokemonDealsTCG posts!

### Check Logs:
```bash
cd /mnt/user/appdata/X_Monitor
docker-compose logs -f
```

### Stop the Monitor:
```bash
docker-compose down
```

### Restart the Monitor:
```bash
docker-compose up -d
```

### Update the Monitor (after making changes on GitHub):
```bash
cd /mnt/user/appdata/X_Monitor
git pull
docker-compose down
docker-compose up -d --build
```

---

## Troubleshooting

### Container won't start:
```bash
docker-compose logs
```
Check for missing environment variables or API errors.

### Not receiving notifications:
- Check Pushbullet app is installed and logged in
- Verify API key is correct
- Check logs for errors

### Want to monitor a different account:
```bash
nano .env
# Change TWITTER_USERNAME to the new account
docker-compose restart
```

---

## Quick Reference Commands

```bash
# Navigate to app
cd /mnt/user/appdata/X_Monitor

# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Update from GitHub
git pull && docker-compose up -d --build
```

---

## ✅ Success Checklist

- [ ] Code pushed to GitHub (without .env file)
- [ ] Cloned to Unraid at `/mnt/user/appdata/X_Monitor`
- [ ] Created `.env` file with real API credentials
- [ ] Got Twitter Bearer Token and added to .env
- [ ] Started with `docker-compose up -d`
- [ ] Checked logs show "Monitoring active"
- [ ] Received test Pushbullet notification

---

**You're all set! The monitor will now alert you instantly when PokemonDealsTCG posts! 🎉**
