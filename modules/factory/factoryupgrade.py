"""
/factoryupgrade command - Upgrade factory
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def factoryupgrade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Upgrade factory"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    factory = db.db.factory.find_one({"user_id": user_id})
    
    if not factory:
        await update.message.reply_text("❌ You don't have a factory yet. Use /factory")
        return
    
    upgrade_cost = factory['level'] * 1000
    
    if not context.args:
        await update.message.reply_text(
            f"⬆️ <b>FACTORY UPGRADE</b>\n\n"
            f"Current Level: {factory['level']}\n"
            f"Upgrade Cost: {upgrade_cost} 💰\n"
            f"Benefits:\n"
            f"• +10% Production\n"
            f"• +5 Worker Capacity\n"
            f"• +1000 💰 Daily\n\n"
            f"Usage: /factoryupgrade confirm",
            parse_mode="HTML"
        )
        return
    
    if context.args[0].lower() != 'confirm':
        return
    
    if user['money'] < upgrade_cost:
        await update.message.reply_text(f"❌ You need {upgrade_cost} 💰")
        return
    
    # Upgrade factory
    db.withdraw_money(user_id, upgrade_cost)
    db.db.factory.update_one(
        {"user_id": user_id},
        {
            "$inc": {
                "level": 1,
                "production": factory['production'] // 10,
                "money_generated": 1000
            }
        }
    )
    
    await update.message.reply_text(
        f"✅ <b>FACTORY UPGRADED!</b>\n\n"
        f"⬆️ New Level: {factory['level'] + 1}\n"
        f"💰 Cost: {upgrade_cost}",
        parse_mode="HTML"
    )
    logger.info(f"Factory upgraded: {user_id} to level {factory['level'] + 1}")

factoryupgrade_handler = CommandHandler('factoryupgrade', factoryupgrade_command)