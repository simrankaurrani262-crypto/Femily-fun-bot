"""
/production command - View production status
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def production_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View production"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    factory = db.db.factory.find_one({"user_id": user_id})
    
    if not factory:
        await update.message.reply_text("❌ You don't have a factory yet. Use /factory")
        return
    
    daily_revenue = factory['workers'] * 100
    monthly_revenue = daily_revenue * 30
    
    production_text = f"""
<b>📊 PRODUCTION STATUS</b>

<b>Daily Production:</b> {factory.get('production', 0)} units
<b>Monthly Production:</b> {factory.get('production', 0) * 30} units

<b>Revenue Calculation:</b>
• Workers: {factory['workers']}
• Per Worker: 100 💰/day
• Daily Revenue: {daily_revenue:,} 💰
• Monthly Revenue: {monthly_revenue:,} 💰

<b>Factory Level:</b> {factory['level']}
<b>Total Generated:</b> {factory.get('money_generated', 0):,} 💰

<b>Next Upgrade Cost:</b> {factory['level'] * 1000} 💰
"""
    
    await update.message.reply_text(production_text, parse_mode="HTML")

production_handler = CommandHandler('production', production_command)