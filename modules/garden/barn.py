"""
/barn command - View barn storage
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def barn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View barn"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    garden = user.get('garden', {})
    barn = garden.get('barn', [])
    
    barn_text = "<b>🥗 BARN STORAGE</b>\n\n"
    
    barn_text += "Items stored:\n"
    for item in barn:
        barn_text += f"• {item}\n"
    
    if not barn:
        barn_text += "Empty"
    
    await update.message.reply_text(barn_text, parse_mode="HTML")

barn_handler = CommandHandler('barn', barn_command)