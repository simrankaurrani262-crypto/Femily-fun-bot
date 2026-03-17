"""
/circle command - View friend circle
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def circle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View friend circle"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    friends = user.get('friends', [])
    
    if not friends:
        await update.message.reply_text("❌ You have no friends yet")
        return
    
    circle_text = f"<b>👥 YOUR FRIEND CIRCLE ({len(friends)})</b>\n\n"
    
    for friend_id in friends:
        friend = db.get_user(friend_id)
        if friend:
            circle_text += f"👤 @{friend['username']}\n"
            circle_text += f"   Level: {friend['level']}\n"
            circle_text += f"   Money: {friend['money']:,} 💰\n\n"
    
    await update.message.reply_text(circle_text, parse_mode="HTML")

circle_handler = CommandHandler('circle', circle_command)