"""
/hire command - Hire workers
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def hire_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hire a worker"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    factory = db.db.factory.find_one({"user_id": user_id})
    
    if not factory:
        await update.message.reply_text("❌ You don't have a factory yet. Use /factory")
        return
    
    if factory['workers'] >= 50:
        await update.message.reply_text("❌ You've reached maximum workers (50)")
        return
    
    hire_cost = 500 + (factory['workers'] * 50)
    
    if not context.args:
        await update.message.reply_text(
            f"👷 <b>HIRE WORKER</b>\n\n"
            f"Cost: {hire_cost} 💰\n"
            f"Current workers: {factory['workers']}/50\n\n"
            f"Usage: /hire confirm",
            parse_mode="HTML"
        )
        return
    
    if context.args[0].lower() != 'confirm':
        return
    
    if user['money'] < hire_cost:
        await update.message.reply_text(f"❌ You need {hire_cost} 💰")
        return
    
    # Hire worker
    db.withdraw_money(user_id, hire_cost)
    db.db.factory.update_one(
        {"user_id": user_id},
        {"$inc": {"workers": 1, "production": 10}}
    )
    
    await update.message.reply_text(
        f"✅ <b>WORKER HIRED!</b>\n\n"
        f"👷 Workers: {factory['workers'] + 1}/50\n"
        f"💰 Cost: {hire_cost}",
        parse_mode="HTML"
    )
    logger.info(f"Worker hired: {user_id} hired worker for {hire_cost}")

hire_handler = CommandHandler('hire', hire_command)