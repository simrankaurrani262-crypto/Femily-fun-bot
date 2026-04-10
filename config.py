"""
Configuration Management for Telegram RPG Bot - Fixed and Enhanced Version
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# ============================================================================
# TELEGRAM CONFIGURATION
# ============================================================================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is required! Please set it in .env file")

ADMIN_IDS = []
admin_ids_str = os.getenv('ADMIN_IDS', '')
if admin_ids_str:
    try:
        ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(',') if x.strip()]
    except ValueError:
        print("⚠️ Warning: Invalid ADMIN_IDS format. Use comma-separated integers.")

# ============================================================================
# MONGODB CONFIGURATION
# ============================================================================
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'telegram_rpg_bot')

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = 'logs/bot.log'

# ============================================================================
# GAME CONFIGURATION - COOLDOWNS (in seconds)
# ============================================================================
COOLDOWN_SECONDS = {
    'daily': 86400,      # 24 hours
    'rob': 3600,         # 1 hour
    'kill': 7200,        # 2 hours
    'work': 1800,        # 30 minutes
    'medical': 3600,     # 1 hour
    'lottery': 86400,    # 24 hours
    'slots': 60,         # 1 minute
    'dice': 30,          # 30 seconds
    'trivia': 300,       # 5 minutes
}

# ============================================================================
# ECONOMY CONFIGURATION
# ============================================================================
DAILY_REWARD = 100
DAILY_STREAK_BONUS = 10  # Additional reward per streak day
MAX_DAILY_STREAK = 7     # Maximum streak days

MAX_MONEY = 999_999_999
MAX_BANK = 9_999_999_999

# Loan Configuration
LOAN_MAX_AMOUNT = 100_000
LOAN_INTEREST_RATE = 0.05  # 5% interest
LOAN_DURATION_DAYS = 7

# Work Configuration
WORK_MIN_EARN = 50
WORK_MAX_EARN = 200
WORK_JOBS = {
    'farmer': {'min': 50, 'max': 150, 'xp': 5},
    'miner': {'min': 80, 'max': 200, 'xp': 8},
    'merchant': {'min': 100, 'max': 250, 'xp': 10},
    'thief': {'min': 30, 'max': 300, 'xp': 15, 'risk': 0.3},
}

# ============================================================================
# FAMILY CONFIGURATION
# ============================================================================
MAX_CHILDREN = 10
MAX_FRIENDS = 100
MAX_WORKERS = 50
MARRIAGE_COST = 1000
DIVORCE_COST = 500
ADOPTION_COST = 500

# ============================================================================
# CRIME CONFIGURATION
# ============================================================================
ROB_SUCCESS_RATE = 0.4
ROB_MIN_AMOUNT = 10
ROB_MAX_AMOUNT = 500
ROB_JAIL_CHANCE = 0.3
ROB_JAIL_DURATION = 30  # minutes

KILL_SUCCESS_RATE = 0.2
KILL_JAIL_CHANCE = 0.5
KILL_JAIL_DURATION = 60  # minutes

# Weapon prices
WEAPONS = {
    'knife': {'price': 500, 'damage': 10, 'rob_bonus': 0.1},
    'pistol': {'price': 2000, 'damage': 25, 'rob_bonus': 0.2},
    'rifle': {'price': 5000, 'damage': 50, 'rob_bonus': 0.3},
}

# Insurance
INSURANCE_COST = 1000
INSURANCE_DURATION = 24  # hours

# ============================================================================
# FACTORY CONFIGURATION
# ============================================================================
FACTORY_UPGRADES = {
    'speed': {'cost': 5000, 'bonus': 0.2},
    'quality': {'cost': 10000, 'bonus': 0.3},
    'automation': {'cost': 25000, 'bonus': 0.5},
}

WORKER_TYPES = {
    'novice': {'salary': 100, 'productivity': 1.0},
    'skilled': {'salary': 250, 'productivity': 1.5},
    'expert': {'salary': 500, 'productivity': 2.5},
}

# ============================================================================
# GARDEN CONFIGURATION
# ============================================================================
CROPS = {
    'wheat': {'seed_cost': 10, 'sell_price': 25, 'growth_time': 300, 'xp': 5},
    'corn': {'seed_cost': 25, 'sell_price': 60, 'growth_time': 600, 'xp': 10},
    'tomato': {'seed_cost': 50, 'sell_price': 130, 'growth_time': 1200, 'xp': 15},
    'pumpkin': {'seed_cost': 100, 'sell_price': 300, 'growth_time': 3600, 'xp': 25},
}

FERTILIZER_COST = 50
FERTILIZER_SPEED_BONUS = 0.5  # 50% faster growth

MAX_PLOTS = 20
PLOT_COST = 1000

# ============================================================================
# GAMES CONFIGURATION
# ============================================================================
# Lottery
LOTTERY_TICKET_PRICE = 50
LOTTERY_JACKPOOL_PERCENTAGE = 0.7

# Blackjack
BLACKJACK_MIN_BET = 10
BLACKJACK_MAX_BET = 10000

# Slots
SLOTS_MIN_BET = 5
SLOTS_MAX_BET = 1000
SLOTS_SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣', '🎰']
SLOTS_PAYOUTS = {
    '🍒🍒🍒': 2,
    '🍋🍋🍋': 3,
    '🍊🍊🍊': 5,
    '🍇🍇🍇': 10,
    '💎💎💎': 25,
    '7️⃣7️⃣7️⃣': 100,
    '🎰🎰🎰': 50,
}

# Dice
DICE_MIN_BET = 10
DICE_MAX_BET = 5000

# Trivia
TRIVIA_REWARD = 50
TRIVIA_TIME_LIMIT = 30  # seconds

# ============================================================================
# MARKET CONFIGURATION
# ============================================================================
MARKET_LISTING_FEE = 10
MARKET_TAX_RATE = 0.05  # 5% tax on sales
AUCTION_DURATION_HOURS = 24

# ============================================================================
# XP AND LEVEL CONFIGURATION
# ============================================================================
XP_PER_LEVEL = 100
LEVEL_REWARDS = {
    5: {'money': 1000, 'item': 'bronze_medal'},
    10: {'money': 5000, 'item': 'silver_medal'},
    25: {'money': 20000, 'item': 'gold_medal'},
    50: {'money': 100000, 'item': 'diamond_medal'},
}

# ============================================================================
# ERROR MESSAGES
# ============================================================================
ERRORS = {
    'not_registered': '❌ You are not registered. Use /start to register.',
    'insufficient_funds': '❌ Insufficient funds.',
    'user_not_found': '❌ User not found.',
    'cooldown': '⏳ Command on cooldown. Wait {time}.',
    'no_permission': '❌ You do not have permission to use this command.',
    'in_jail': '🚔 You are in jail! Wait {time} to be released.',
    'already_married': '💔 You are already married!',
    'not_married': '💔 You are not married!',
    'max_children': '👶 You have reached the maximum number of children.',
    'max_friends': '👥 You have reached the maximum number of friends.',
    'max_workers': '👷 You have reached the maximum number of workers.',
    'invalid_amount': '❌ Invalid amount specified.',
    'item_not_found': '❌ Item not found in your inventory.',
}

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================
SUCCESS = {
    'registered': '✅ Welcome! You have been registered with 500💰 starter money!',
    'daily_claimed': '✅ Daily reward claimed: {amount}💰 (Streak: {streak} days)',
    'payment_sent': '✅ Sent {amount}💰 to {recipient}',
    'payment_received': '💰 You received {amount}💰 from {sender}',
    'married': '💍 Congratulations! You are now married to {partner}!',
    'divorced': '💔 You are now divorced.',
    'adopted': '👶 You have adopted {child}!',
    'friend_added': '👥 You are now friends with {friend}!',
    'item_purchased': '✅ Purchased {item} for {price}💰',
    'item_sold': '✅ Sold {item} for {price}💰',
}

# ============================================================================
# SHOP ITEMS
# ============================================================================
SHOP_ITEMS = {
    'fertilizer': {'price': 50, 'description': 'Speeds up crop growth by 50%'},
    'seed_wheat': {'price': 10, 'description': 'Wheat seeds for farming'},
    'seed_corn': {'price': 25, 'description': 'Corn seeds for farming'},
    'seed_tomato': {'price': 50, 'description': 'Tomato seeds for farming'},
    'lottery_ticket': {'price': 50, 'description': 'Try your luck in the lottery!'},
    'insurance': {'price': 1000, 'description': 'Protects you from crimes for 24 hours'},
}
