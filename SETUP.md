# 🚀 TELEGRAM RPG BOT - SETUP GUIDE

## Prerequisites

- Python 3.11 or higher
- MongoDB (local or Atlas)
- Telegram Bot Token (from @BotFather)

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/simrankaurrani262-crypto/telegram-rpg-bot.git
cd telegram-rpg-bot
```

### 2. Create Virtual Environment

```bash
# macOS / Linux
python3.11 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup MongoDB

#### Option A: Local MongoDB

**macOS (with Homebrew):**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
```

**Windows:**
Download from https://www.mongodb.com/try/download/community

#### Option B: MongoDB Atlas (Cloud)

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a cluster
4. Get connection string
5. Update `.env` with your URI

### 5. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your values
nano .env
```

**Fill in these values:**

```env
TELEGRAM_TOKEN=your_bot_token_here
MONGO_URI=mongodb://localhost:27017
# or for MongoDB Atlas:
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
ADMIN_IDS=your_telegram_id
LOG_LEVEL=INFO
```

**How to get your Telegram Bot Token:**
1. Open Telegram
2. Search for @BotFather
3. Type `/start`
4. Type `/newbot`
5. Follow instructions and copy the token

**How to get your Telegram ID:**
1. Search for @userinfobot
2. Type `/start`
3. It will show your ID

### 6. Run the Bot

```bash
python bot.py
```

You should see:
```
2026-03-07 10:00:00 - bot - INFO - ✅ MongoDB connected successfully
2026-03-07 10:00:00 - bot - INFO - 📝 Registering command handlers...
2026-03-07 10:00:00 - bot - INFO - ✅ All handlers registered
2026-03-07 10:00:00 - bot - INFO - 🚀 Bot is running...
```

### 7. Test the Bot

Open Telegram and:
1. Find your bot (search by name or @username)
2. Type `/start`
3. You should be registered!
4. Try `/help` to see all commands
5. Try `/profile` to see your profile
6. Try `/tree` to generate your family tree

---

## 🐳 Using Docker

### With Docker Compose (Easiest)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

### With Docker Only

```bash
# Build image
docker build -t telegram-rpg-bot .

# Run container
docker run -d \
  -e TELEGRAM_TOKEN=your_token \
  -e MONGO_URI=mongodb://mongo:27017 \
  --name telegram-rpg-bot \
  telegram-rpg-bot
```

---

## ✅ Common Issues & Fixes

### Issue: "ModuleNotFoundError: No module named 'telegram'"

**Fix:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Connection refused" (MongoDB)

**Fix:** Make sure MongoDB is running
```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongodb

# Check status
mongo --version
```

### Issue: "Invalid token"

**Fix:** Get a new token from @BotFather and update `.env`

### Issue: "bot.send_message() got an unexpected keyword argument"

**Fix:** Update python-telegram-bot
```bash
pip install --upgrade python-telegram-bot
```

---

## 📝 Project Structure

```
telegram_rpg_bot/
├── bot.py                 # Main entry
├── config.py              # Configuration
├── database.py            # MongoDB
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── README.md             # Documentation
│
└── modules/
    ├── core/            # Core features
    ├── family/          # Family system
    ├── economy/         # Economy
    ├── crime/           # Crime
    ├── factory/         # Factory
    ├── garden/          # Farming
    ├── market/          # Market
    ├── games/           # Games
    ├── stats/           # Stats
    ├── admin/           # Admin
    └── utils/           # Utilities
```

---

## 🚀 Development

### Adding a New Command

1. Create file in appropriate module: `modules/feature/command.py`
2. Implement async handler
3. Import in `bot.py`
4. Add to handlers list

**Example:**

```python
# modules/feature/mycommand.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

my_handler = CommandHandler('mycommand', my_command)
```

```python
# bot.py
from modules.feature.mycommand import my_handler

app.add_handler(my_handler)
```

### Adding a New Module

1. Create folder: `modules/newmodule/`
2. Create `__init__.py`
3. Add feature files
4. Import handlers in `bot.py`

---

## 📊 Monitoring

### View Logs

```bash
tail -f logs/bot.log
```

### MongoDB Queries

```bash
# Connect to MongoDB
mongo

# Use database
use telegram_rpg_bot

# View users
db.users.find().pretty()

# View families
db.families.find().pretty()
```

---

## 🔒 Security Tips

- Keep `.env` file secret (never commit it)
- Use environment variables for all secrets
- Validate all user inputs
- Implement rate limiting
- Add CSRF protection if using web interface
- Regularly update dependencies

---

## 📈 Scaling

### For Thousands of Users

1. **Use MongoDB Atlas** for cloud database
2. **Add Redis** for caching
3. **Use multiple bot instances** with message queue
4. **Implement load balancer** for requests
5. **Add database indexing** for query optimization

---

## 🆘 Support

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Bot Issues**: Try `/help` in the bot

---

**Happy coding! 🎉**