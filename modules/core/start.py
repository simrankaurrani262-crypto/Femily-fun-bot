"""
/start command handler - Registration
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    user_id = update.effective_user.id
    username = update.effective_user.username or f"user{user_id}"
    first_name = update.effective_user.first_name or "Player"
    
    user = db.get_user(user_id)
    
    if user:
        # Returning user - UPDATE first_name and username if they changed
        db.update_user(user_id, {
            'first_name': first_name,
            'username': username
        })
        
        keyboard = [
            [
                InlineKeyboardButton("👤 Profile", callback_data="profile"),
                InlineKeyboardButton("🎮 Play", callback_data="games"),
            ],
            [
                InlineKeyboardButton("👨‍👩‍👧‍👦 Family", callback_data="family"),
                InlineKeyboardButton("💰 Economy", callback_data="economy"),
            ],
            [
                InlineKeyboardButton("📊 Stats", callback_data="stats"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
            ]
        ]
        
        await update.message.reply_text(
            f"<b>Welcome back, {first_name}! 👋</b>\n\n"
            f"Use the buttons below or type /help for commands.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        # New user - CREATE with first_name and username
        user_doc = db.create_user(user_id, username, first_name)
        
        keyboard = [
            [InlineKeyboardButton("📖 Read Guide", callback_data="guide")],
            [InlineKeyboardButton("👤 View Profile", callback_data="profile")],
        ]
        
        await update.message.reply_text(
            f"<b>🎮 Welcome to Telegram RPG Bot, {first_name}! 🎮</b>\n\n"
            f"You've been registered! You start with:\n"
            f"💰 500 coins\n"
            f"📊 Level 1\n\n"
            f"<b>Quick Start:</b>\n"
            f"/family - View family tree\n"
            f"/daily - Claim daily rewards\n"
            f"/profile - View your profile\n"
            f"/help - See all commands\n\n"
            f"<i>Good luck, and have fun!</i>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        logger.info(f"✅ New user registered: {user_id} ({username})")

start_handler = CommandHandler('start', start)
