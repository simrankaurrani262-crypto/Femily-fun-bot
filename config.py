"""
Configuration Management for Telegram RPG Bot
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv(Path(__file__).parent / '.env')

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(','))) if os.getenv('ADMIN_IDS') else []

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = 'telegram_rpg_bot'

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = 'logs/bot.log'

# Game Configuration
COOLDOWN_SECONDS = {
    'daily': 86400,
    'rob': 3600,
    'kill': 7200,
    'work': 1800,
    'medical': 3600,
}

# Economy Configuration
DAILY_REWARD = 100
MAX_MONEY = 999999999
MAX_BANK = 9999999999

# Family Configuration
MAX_CHILDREN = 10
MAX_FRIENDS = 100
MAX_WORKERS = 50

# Error Messages
ERRORS = {
    'not_registered': '❌ You are not registered. Use /start to register.',
    'insufficient_funds': '❌ Insufficient funds.',
    'user_not_found': '❌ User not found.',
    'cooldown': '⏳ Command on cooldown for {time}s.',
    'no_permission': '❌ You do not have permission to use this command.',
}

# Success Messages
SUCCESS = {
    'registered': '✅ You have been registered!',
    'daily_claimed': '✅ Daily reward claimed: {amount}💰',
}