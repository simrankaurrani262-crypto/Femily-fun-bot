"""
/factory command - View factory
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def factory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View factory"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    factory = db.db.factory.find_one({"user_id": user_id})
    
    if not factory:
        # Create factory
        db.db.factory.insert_one({
            "user_id": user_id,
            "level": 1,
            "workers": 0,
            "production": 0,
            "money_generated": 0,
            "upgrades": {}
        })
        factory = db.db.factory.find_one({"user_id": user_id})
    
    factory_text = f"""
<b>🏭 YOUR FACTORY</b>

<b>Level:</b> {factory['level']}
<b>Workers:</b> {factory['workers']} / 50
<b>Production:</b> {factory['production']} units

<b>Money Generated:</b> {factory.get('money_generated', 0):,} 💰

<b>Upgrades:</b>
• Assembly Line Level {factory.get('upgrades', {}).get('assembly', 0)}
• Conveyor System Level {factory.get('upgrades', {}).get('conveyor', 0)}
"""
    
    keyboard = [
        [
            InlineKeyboardButton("👷 Hire Worker", callback_data="factory_hire"),
            InlineKeyboardButton("🚪 Fire Worker", callback_data="factory_fire"),
        ],
        [
            InlineKeyboardButton("👥 Workers", callback_data="factory_workers"),
            InlineKeyboardButton("⬆️ Upgrade", callback_data="factory_upgrade"),
        ],
    ]
    
    await update.message.reply_text(
        factory_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

factory_handler = CommandHandler('factory', factory_command)