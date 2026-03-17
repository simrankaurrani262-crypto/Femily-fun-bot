"""
/unfriend command - Remove friend
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def unfriend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove friend"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "❌ <b>REMOVE FRIEND</b>\n\n"
            "Usage: /unfriend @username",
            parse_mode="HTML"
        )
        return
    
    target_username = context.args[0].lstrip('@')
    target = db.db.users.find_one({"username": target_username})
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target['user_id'] not in user.get('friends', []):
        await update.message.reply_text(f"❌ @{target['username']} is not your friend")
        return
    
    # Remove friend
    db.db.users.update_one(
        {"user_id": user_id},
        {"$pull": {"friends": target['user_id']}}
    )
    
    await update.message.reply_text(
        f"✅ <b>FRIEND REMOVED</b>\n\n"
        f"❌ @{target['username']} is no longer your friend",
        parse_mode="HTML"
    )

unfriend_handler = CommandHandler('unfriend', unfriend_command)