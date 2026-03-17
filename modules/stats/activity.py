"""
/activity command - Most active players
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def activity_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Most active players"""
    user_id = update.effective_user.id
    
    users = db.get_leaderboard('experience', 10)
    
    activity_text = "<b>⚡ MOST ACTIVE PLAYERS</b>\n\n"
    
    for idx, user in enumerate(users, 1):
        activity_text += f"{idx}. @{user['username']}\n"
        activity_text += f"   XP: {user['experience']}\n"
        activity_text += f"   Level: {user['level']}\n\n"
    
    await update.message.reply_text(activity_text, parse_mode="HTML")

activity_handler = CommandHandler('activity', activity_command)