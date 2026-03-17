"""
/fire command - Fire workers
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def fire_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fire a worker"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    factory = db.db.factory.find_one({"user_id": user_id})
    
    if not factory or factory['workers'] <= 0:
        await update.message.reply_text("❌ You have no workers to fire")
        return
    
    if not context.args or context.args[0].lower() != 'confirm':
        await update.message.reply_text(
            f"⚠️ <b>FIRE WORKER</b>\n\n"
            f"Current workers: {factory['workers']}\n"
            f"Production will decrease by 10\n\n"
            f"Usage: /fire confirm",
            parse_mode="HTML"
        )
        return
    
    # Fire worker
    db.db.factory.update_one(
        {"user_id": user_id},
        {"$inc": {"workers": -1, "production": -10}}
    )
    
    await update.message.reply_text(
        f"✅ <b>WORKER FIRED</b>\n\n"
        f"👷 Workers: {factory['workers'] - 1}",
        parse_mode="HTML"
    )
    logger.info(f"Worker fired: {user_id} fired a worker")

fire_handler = CommandHandler('fire', fire_command)