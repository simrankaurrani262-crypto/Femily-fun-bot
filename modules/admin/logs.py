"""
/logs command - View bot logs
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from config import ADMIN_IDS
import logging

logger = logging.getLogger(__name__)

async def logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View logs"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You do not have permission")
        return
    
    try:
        with open('logs/bot.log', 'r') as f:
            logs = f.readlines()[-20:]  # Last 20 lines
        
        logs_text = "<b>📋 RECENT LOGS</b>\n\n"
        logs_text += "".join(logs[-10:])  # Last 10
        
        await update.message.reply_text(f"<pre>{logs_text}</pre>", parse_mode="HTML")
    except:
        await update.message.reply_text("❌ Could not read logs")

logs_handler = CommandHandler('logs', logs_command)