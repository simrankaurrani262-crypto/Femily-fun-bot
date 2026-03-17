"""
/broadcast command - Send message to all users
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
from config import ADMIN_IDS
import logging

logger = logging.getLogger(__name__)

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all users"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You do not have permission")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 <b>BROADCAST</b>\n\n"
            "Usage: /broadcast message_text",
            parse_mode="HTML"
        )
        return
    
    message = ' '.join(context.args)
    
    # Get all users
    all_users = db.db.users.find({"banned": False})
    
    sent_count = 0
    for user in all_users:
        try:
            await context.bot.send_message(
                chat_id=user['user_id'],
                text=f"📢 <b>ANNOUNCEMENT</b>\n\n{message}",
                parse_mode="HTML"
            )
            sent_count += 1
        except:
            pass
    
    await update.message.reply_text(
        f"✅ <b>BROADCAST SENT</b>\n\n"
        f"📢 Sent to {sent_count} users",
        parse_mode="HTML"
    )
    logger.info(f"Broadcast: {user_id} sent message to {sent_count} users")

broadcast_handler = CommandHandler('broadcast', broadcast_command)