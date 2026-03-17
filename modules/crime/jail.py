"""
/jail command - Check jail status
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def jail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check jail status"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    jail_time = user.get('jail_time', 0)
    
    if jail_time <= 0:
        await update.message.reply_text("✅ You are not in jail")
    else:
        jail_text = f"""
<b>🚔 JAIL STATUS</b>

⏳ Time remaining: {jail_time} hours

Use /bail to get out early
"""
        await update.message.reply_text(jail_text, parse_mode="HTML")

jail_handler = CommandHandler('jail', jail_command)