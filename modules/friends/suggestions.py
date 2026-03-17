"""
/suggestions command - Get friend suggestions
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import random
import logging

logger = logging.getLogger(__name__)

async def suggestions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get friend suggestions"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    current_friends = set(user.get('friends', []))
    
    # Get random users not in friends list
    all_users = list(db.db.users.find(
        {"user_id": {"$ne": user_id}, "banned": False},
        {"user_id": 1, "username": 1, "level": 1}
    ).limit(100))
    
    suggestions = [u for u in all_users if u['user_id'] not in current_friends]
    random.shuffle(suggestions)
    suggestions = suggestions[:10]
    
    if not suggestions:
        await update.message.reply_text("❌ No friend suggestions available")
        return
    
    suggestions_text = "<b>🤝 FRIEND SUGGESTIONS</b>\n\n"
    
    for suggestion in suggestions:
        suggestions_text += f"@{suggestion['username']} - Level {suggestion['level']}\n"
    
    keyboard = [
        [InlineKeyboardButton(f"Add @{s['username']}", 
         callback_data=f"add_friend_{s['user_id']}")] 
        for s in suggestions[:5]
    ]
    
    await update.message.reply_text(
        suggestions_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Suggestions viewed by {user_id}")

suggestions_handler = CommandHandler('suggestions', suggestions_command)