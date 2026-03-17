# 🎮 Telegram RPG Bot

A **production-ready**, **scalable**, and **modular** Telegram RPG simulation bot inspired by family-tree life simulation games.

## ✨ Features

- **👨‍👩‍👧‍👦 Family Tree Generator**: Dynamically generates PNG images showing complete family structures
- **💰 Full Economy System**: Money, bank, loans, transactions
- **⚔️ Crime System**: Rob, kill, weapons, jail, insurance
- **🏭 Factory System**: Hire workers, production, upgrades
- **🌾 Garden/Farming**: Plant, harvest, fertilize, barn storage
- **🛒 Market System**: Buy, sell, trade, auctions, gifts
- **🎲 Games**: 10+ mini-games (lottery, blackjack, slots, etc.)
- **📊 Leaderboards**: Money, family, factory, activity rankings
- **👥 Friend System**: Add friends, ratings, suggestions
- **⚙️ Admin Panel**: Ban users, broadcast, view logs
- **📈 300+ Commands**: Complete command system for all features

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Telegram Framework**: `python-telegram-bot` (async)
- **Database**: MongoDB with PyMongo
- **Image Generation**: Pillow, NetworkX, Matplotlib
- **Scheduling**: APScheduler
- **Environment**: python-dotenv

## 📋 Requirements

```
python-telegram-bot[async]>=20.0
pymongo>=4.4
python-dotenv
Pillow
networkx
matplotlib
APScheduler
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/simrankaurrani262-crypto/telegram-rpg-bot.git
cd telegram-rpg-bot
```

### 2. Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MongoDB
```bash
# Option A: Local MongoDB
mongod

# Option B: MongoDB Atlas
# Create account at https://www.mongodb.com/cloud/atlas
```

### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env with your values:
# - TELEGRAM_TOKEN (get from @BotFather)
# - MONGO_URI
# - ADMIN_IDS
```

### 6. Run Bot
```bash
python bot.py
```

## 📁 Project Structure

```
telegram_rpg_bot/
├── bot.py                    # Main entry point
├── config.py                 # Configuration management
├── database.py               # MongoDB operations
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── README.md                 # This file
│
├── modules/
│   ├── core/                 # Core features
│   │   ├── start.py
│   │   ├── help.py
│   │   ├── profile.py
│   │   └── settings.py
│   │
│   ├── family/               # Family system
│   │   ├── family.py
│   │   ├── tree.py
│   │   ├── adopt.py
│   │   ├── marry.py
│   │   ├── divorce.py
│   │   └── relations.py
│   │
│   ├── economy/              # Economy system
│   │   ├── daily.py
│   │   ├── account.py
│   │   ├── pay.py
│   │   ├── jobs.py
│   │   ├── inventory.py
│   │   └── shop.py
│   │
│   ├── crime/                # Crime system
│   │   ├── rob.py
│   │   ├── kill.py
│   │   ├── weapons.py
│   │   └── jail.py
│   │
│   ├── factory/              # Factory system
│   │   ├── factory.py
│   │   ├── hire.py
│   │   └── production.py
│   │
│   ├── garden/               # Farming system
│   │   ├── garden.py
│   │   ├── plant.py
│   │   └── harvest.py
│   │
│   ├── market/               # Market system
│   │   ├── stand.py
│   │   ├── trade.py
│   │   └── auction.py
│   │
│   ├── games/                # Mini-games
│   │   ├── lottery.py
│   │   ├── blackjack.py
│   │   ├── slots.py
│   │   └── ...
│   │
│   ├── stats/                # Statistics & leaderboards
│   │   ├── leaderboard.py
│   │   ├── moneyboard.py
│   │   └── moneygraph.py
│   │
│   ├── admin/                # Admin commands
│   │   ├── ban.py
│   │   ├── broadcast.py
│   │   └── logs.py
│   │
│   └── utils/                # Utilities
│       ├── tree_generator.py # Family tree image generator
│       ├── cooldown.py
│       ├── helpers.py
│       ├── validators.py
│       └── logger.py
```

## 🎮 Main Commands

### Core
```
/start       - Register/start bot
/help        - View help
/profile     - View profile
/settings    - Change settings
```

### Family
```
/family      - View family info
/tree        - Generate family tree (IMAGE)
/fulltree    - View full family structure
/marry       - Marry someone
/adopt       - Adopt someone
/children    - View children
```

### Economy
```
/daily       - Claim daily reward (100💰)
/account     - View balance
/pay         - Pay another player
/job         - View jobs
/shop        - Browse shop
```

### Crime
```
/rob         - Rob another player
/kill        - Attack someone
/jail        - Check jail status
```

### Games
```
/lottery     - Buy lottery ticket
/blackjack   - Play blackjack
/slots       - Play slots
```

### Leaderboards
```
/leaderboard - Top players
/moneyboard  - Richest players
/familyboard - Largest families
```

## 🗄️ MongoDB Collections

```javascript
// Users
{
  user_id: Number,
  username: String,
  money: Number,
  bank: Number,
  level: Number,
  experience: Number,
  partner: ObjectId,
  children: [ObjectId],
  parents: [ObjectId],
  job: String,
  banned: Boolean,
  // ... more fields
}

// Families
{
  user_id: Number,
  partner: Number,
  children: [Number],
  parents: [Number],
  grandparents: [Number],
  grandchildren: [Number]
}

// Friends, Economy, Gardens, Factory, Market, Games, Stats
```

## 🖼️ Family Tree Generator

The bot includes a sophisticated **family tree image generator** that:

- ✅ Creates NetworkX directed graphs from family data
- ✅ Applies hierarchical layout algorithm
- ✅ Renders with Matplotlib with custom colors
- ✅ Exports to high-quality PNG images
- ✅ Supports up to 7 generations
- ✅ Color-codes by relationship type

**Example Output**: A visual family tree showing:
- 🧑 You (blue)
- ❤️ Partner (red)
- 👪 Parents (green)
- 👶 Children (yellow)
- 🧓 Grandparents (brown)
- 👦 Grandchildren (purple)

## 🔧 Configuration

Edit `.env`:

```env
TELEGRAM_TOKEN=YOUR_BOT_TOKEN
MONGO_URI=mongodb://localhost:27017
ADMIN_IDS=123456789
LOG_LEVEL=INFO
```

## 📊 Database Setup

### Local MongoDB
```bash
# Install MongoDB
brew install mongodb-community  # Mac
sudo apt-get install mongodb    # Linux

# Start MongoDB
brew services start mongodb-community  # Mac
sudo systemctl start mongod            # Linux

# MongoDB will be available at mongodb://localhost:27017
```

### MongoDB Atlas (Cloud)
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create cluster
3. Get connection string
4. Add to `.env`: `MONGO_URI=mongodb+srv://...`

## 📈 Scaling Considerations

The bot is designed to handle **thousands of concurrent users**:

- ✅ **Async/Await**: All handlers use async pattern
- ✅ **Connection Pooling**: MongoDB connection pooling
- ✅ **Cooldown System**: Prevents abuse and server load
- ✅ **Indexed Database**: Optimized queries
- ✅ **Modular Architecture**: Easy to scale horizontally

### Future Enhancements
- Redis caching for leaderboards
- Message queue for heavy operations
- Horizontal scaling with multiple bot instances
- Database sharding for 1M+ users

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request

## 📝 License

Apache 2.0 - See LICENSE file

## 🆘 Support

- 📖 Documentation: See `/help` in bot
- 🐛 Report bugs: Open an issue
- 💡 Feature requests: Discuss in issues
- ❓ Questions: Contact via Telegram

---

**Made with ❤️ by simrankaurrani262-crypto**

⭐ If you found this useful, please star the repository!