"""
/workers command - View factory workers
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def workers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View workers"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    factory = db.db.factory.find_one({"user_id": user_id})
    
    if not factory:
        await update.message.reply_text("❌ You don't have a factory yet. Use /factory")
        return
    
    workers_text = f"""
<b>👷 FACTORY WORKERS</b>

<b>Total Workers:</b> {factory['workers']}/50
<b>Production Capacity:</b> {factory['workers'] * 10} units/day
<b>Productivity:</b> {factory['workers'] * 5}%

<b>Worker Types:</b>
• Assembly Workers: {factory['workers'] // 2}
• Quality Control: {factory['workers'] // 4}
• Management: {factory['workers'] // 6}

<b>Daily Production:</b> {factory.get('production', 0)} units
<b>Efficiency:</b> {min(100, (factory.get('production', 0) / (factory['workers'] * 10)) * 100):.1f}%
"""
    
    await update.message.reply_text(workers_text, parse_mode="HTML")

workers_handler = CommandHandler('workers', workers_command)