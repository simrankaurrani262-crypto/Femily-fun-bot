"""
/unban command - Unban user (Admin only)
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
from config import ADMIN_IDS
import logging

logger = logging.getLogger(__name__)

async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban a user"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You do not have permission")
        return
    
    if not context.args:
        await update.message.reply_text(
            "✅ <b>UNBAN USER</b>\n\n"
            "Usage: /unban @username",
            parse_mode="HTML"
        )
        return
    
    target_username = context.args[0].lstrip('@')
    target = db.db.users.find_one({"username": target_username})
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    db.unban_user(target['user_id'])
    
    await update.message.reply_text(
        f"✅ <b>USER UNBANNED</b>\n\n"
        f"User: @{target['username']}",
        parse_mode="HTML"
    )
    logger.info(f"User unbanned: {target['user_id']}")

unban_handler = CommandHandler('unban', unban_command)