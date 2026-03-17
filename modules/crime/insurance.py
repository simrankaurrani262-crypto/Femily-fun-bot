"""
/insurance command - Insurance system
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

INSURANCE_TYPES = {
    "basic": {"cost": 100, "protection": 500, "emoji": "🛡️"},
    "standard": {"cost": 250, "protection": 1500, "emoji": "🛡️🛡️"},
    "premium": {"cost": 500, "protection": 5000, "emoji": "🛡️🛡️🛡️"},
    "platinum": {"cost": 1000, "protection": 15000, "emoji": "🛡️🛡️🛡️🛡️"},
}

async def insurance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View insurance"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    insurance_text = "<b>🛡️ INSURANCE PLANS</b>\n\n"
    
    for plan_name, plan_info in INSURANCE_TYPES.items():
        insurance_text += f"{plan_info['emoji']} {plan_name.capitalize()}\n"
        insurance_text += f"   Monthly: {plan_info['cost']} 💰\n"
        insurance_text += f"   Coverage: {plan_info['protection']} 💰\n\n"
    
    insurance_text += f"\n<b>Your Current Insurance:</b> {user.get('insurance', 0)} 💰"
    
    await update.message.reply_text(insurance_text, parse_mode="HTML")

insurance_handler = CommandHandler('insurance', insurance_command)