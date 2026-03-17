"""
/medical command - Get medical help
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
from modules.utils.cooldown import CooldownManager
import logging

logger = logging.getLogger(__name__)

async def medical_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get medical treatment"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    # Check cooldown
    can_heal, remaining = CooldownManager.check_cooldown(user_id, 'medical', 3600)
    if not can_heal:
        minutes = int(remaining // 60)
        await update.message.reply_text(f"⏳ You can use medical again in {minutes}m")
        return
    
    treatment_cost = 200
    
    if user['money'] < treatment_cost:
        await update.message.reply_text(f"❌ Medical treatment costs {treatment_cost} 💰")
        return
    
    # Get treatment
    db.withdraw_money(user_id, treatment_cost)
    CooldownManager.set_cooldown(user_id, 'medical')
    
    await update.message.reply_text(
        f"✅ <b>MEDICAL TREATMENT COMPLETE</b>\n\n"
        f"💉 You're feeling better!\n"
        f"Cost: {treatment_cost} 💰",
        parse_mode="HTML"
    )
    logger.info(f"Medical: {user_id} got treatment")

medical_handler = CommandHandler('medical', medical_command)