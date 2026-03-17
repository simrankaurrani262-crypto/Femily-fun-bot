"""
/daily command - Claim daily rewards
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
from modules.utils.cooldown import CooldownManager
from config import DAILY_REWARD
import logging

logger = logging.getLogger(__name__)

async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Claim daily reward"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    # Check cooldown
    can_claim, remaining = CooldownManager.check_cooldown(user_id, 'daily', 86400)
    
    if not can_claim:
        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        await update.message.reply_text(
            f"⏳ You already claimed today! Try again in {hours}h {minutes}m"
        )
        return
    
    # Award money
    db.add_money(user_id, DAILY_REWARD)
    CooldownManager.set_cooldown(user_id, 'daily')
    
    await update.message.reply_text(
        f"✅ Daily reward claimed!\n\n"
        f"💰 +{DAILY_REWARD} coins\n"
        f"Total: {user['money'] + DAILY_REWARD:,} 💰"
    )
    logger.info(f"Daily reward claimed by {user_id}")

daily_handler = CommandHandler('daily', daily_command)