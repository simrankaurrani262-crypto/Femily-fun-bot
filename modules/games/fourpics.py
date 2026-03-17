"""
/4p command - Four Pics One Word
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import random
import logging

logger = logging.getLogger(__name__)

FOUR_PICS = [
    {"pics": "🐱🐱🐱🐱", "answer": "cat", "reward": 100},
    {"pics": "🐕🐕🐕🐕", "answer": "dog", "reward": 100},
    {"pics": "🍎🍎🍎🍎", "answer": "apple", "reward": 100},
    {"pics": "🌊🌊🌊🌊", "answer": "ocean", "reward": 150},
    {"pics": "⭐⭐⭐⭐", "answer": "star", "reward": 100},
]

async def fourpics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Four Pics One Word"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    pics_data = random.choice(FOUR_PICS)
    
    context.user_data['4pics'] = pics_data
    
    await update.message.reply_text(
        f"""
<b>🖼️ FOUR PICS ONE WORD</b>

{pics_data['pics']}

What word do these pictures represent?

<i>Reply with your answer</i>

<b>Reward:</b> {pics_data['reward']} 💰
""",
        parse_mode="HTML"
    )

fourpics_handler = CommandHandler('4p', fourpics_command)