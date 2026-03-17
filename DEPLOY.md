# 🚀 DEPLOYMENT GUIDE

## Deployment Options

### 1. **Local Machine** (Development)

Already covered in SETUP.md

### 2. **Heroku** (Free/Easy)

**Step 1: Install Heroku CLI**
```bash
brew tap heroku/brew && brew install heroku
```

**Step 2: Login**
```bash
heroku login
```

**Step 3: Create App**
```bash
heroku create your-app-name
```

**Step 4: Add MongoDB Atlas**
```bash
heroku addons:create mongolab:sandbox
```

**Step 5: Set Environment Variables**
```bash
heroku config:set TELEGRAM_TOKEN=your_token
heroku config:set ADMIN_IDS=your_id
```

**Step 6: Deploy**
```bash
git push heroku main
```

**Step 7: Monitor**
```bash
heroku logs --tail
```

### 3. **AWS EC2**

**Step 1: Launch EC2 Instance**
- Choose Ubuntu 20.04 LTS
- Security group: Allow SSH (22), HTTP (80), HTTPS (443)

**Step 2: SSH Into Server**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

**Step 3: Update System**
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

**Step 4: Install Dependencies**
```bash
sudo apt-get install -y python3.11 python3-pip git mongodb
```

**Step 5: Clone Repository**
```bash
git clone https://github.com/your-username/telegram-rpg-bot.git
cd telegram-rpg-bot
```

**Step 6: Setup Virtual Environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Step 7: Configure Environment**
```bash
cp .env.example .env
nano .env
# Add your values
```

**Step 8: Setup Systemd Service**
```bash
sudo nano /etc/systemd/system/telegram-rpg-bot.service
```

Add:
```ini
[Unit]
Description=Telegram RPG Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/telegram-rpg-bot
Environment="PATH=/home/ubuntu/telegram-rpg-bot/venv/bin"
ExecStart=/home/ubuntu/telegram-rpg-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Step 9: Enable Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-rpg-bot
sudo systemctl start telegram-rpg-bot
```

**Step 10: Check Status**
```bash
sudo systemctl status telegram-rpg-bot
sudo journalctl -u telegram-rpg-bot -f
```

### 4. **DigitalOcean App Platform**

**Step 1: Connect Repository**
- Push to GitHub
- Go to DigitalOcean App Platform
- Create new app
- Connect your GitHub repository

**Step 2: Set Environment**
- Add TELEGRAM_TOKEN
- Add MONGO_URI
- Add ADMIN_IDS

**Step 3: Deploy**
- DigitalOcean will build and deploy automatically

### 5. **VPS with Docker** (Recommended)

**Step 1: SSH Into VPS**
```bash
ssh root@your-vps-ip
```

**Step 2: Install Docker**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

**Step 3: Clone Repository**
```bash
git clone https://github.com/your-username/telegram-rpg-bot.git
cd telegram-rpg-bot
```

**Step 4: Create .env File**
```bash
cp .env.example .env
nano .env
```

**Step 5: Start with Docker Compose**
```bash
docker-compose up -d
```

**Step 6: Monitor Logs**
```bash
docker-compose logs -f bot
```

**Step 7: Stop**
```bash
docker-compose down
```

---

## Production Checklist

- [ ] Environment variables configured
- [ ] MongoDB backup enabled
- [ ] Logs being collected
- [ ] Error handling implemented
- [ ] Rate limiting enabled
- [ ] Database indexes created
- [ ] Security groups configured
- [ ] SSL/TLS certificates (if using web)
- [ ] Monitoring set up
- [ ] Backup strategy defined

---

## Performance Optimization

### 1. Database Optimization

```javascript
// Create indexes
db.users.createIndex({ "user_id": 1 }, { unique: true })
db.families.createIndex({ "user_id": 1 })
db.friends.createIndex({ "user_id": 1 })
```

### 2. Caching with Redis

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Cache user data
redis_client.setex(f'user:{user_id}', 3600, user_json)
```

### 3. Connection Pooling

Configured in PyMongo automatically

### 4. Async Operations

All handlers use async/await

---

## Monitoring & Maintenance

### Logging

```bash
# View logs
tail -f logs/bot.log

# Search for errors
grep ERROR logs/bot.log
```

### Backups

```bash
# MongoDB backup
mongodump --uri "mongodb://localhost:27017" --out ./backup

# Restore
mongorestore --uri "mongodb://localhost:27017" ./backup
```

### Restarts

```bash
# Restart service
sudo systemctl restart telegram-rpg-bot

# Check status
sudo systemctl status telegram-rpg-bot
```

---

## Troubleshooting

### Bot Not Responding

1. Check logs: `sudo journalctl -u telegram-rpg-bot -f`
2. Verify token: Check `.env` file
3. Check MongoDB: `mongo` connection
4. Restart bot: `sudo systemctl restart telegram-rpg-bot`

### Database Connection Error

1. Check MongoDB status: `sudo systemctl status mongodb`
2. Verify connection string in `.env`
3. Check MongoDB is listening: `ss -tlnp | grep 27017`

### High Memory Usage

1. Check for memory leaks
2. Restart bot
3. Scale horizontally with multiple instances

---

## Cost Estimation (Monthly)

| Service | Free Tier | Paid (Small) |
|---------|-----------|-------------|
| Heroku | ✅ | $7-50 |
| AWS EC2 | 1 year free | $5-20 |
| DigitalOcean | ❌ | $5-20 |
| MongoDB Atlas | ✅ 512MB | $3-100 |
| **Total** | **Free** | **$8-70** |

---

**Happy Deploying! 🚀**