"""
/adminstats command - Admin statistics
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
from config import ADMIN_IDS
import logging

logger = logging.getLogger(__name__)

async def adminstats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin statistics"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You do not have permission")
        return
    
    total_users = db.db.users.count_documents({})
    banned_users = db.db.users.count_documents({"banned": True})
    active_users = db.db.users.count_documents({"last_daily": {"$exists": True, "$ne": None}})
    
    stats_text = f"""
<b>📊 ADMIN STATISTICS</b>

<b>Users:</b>
• Total: {total_users}
• Banned: {banned_users}
• Active: {active_users}

<b>Economy:</b>
• Total Money in Game: {sum(u['money'] + u['bank'] for u in db.db.users.find({}, {'money': 1, 'bank': 1}))} 💰

<b>Families:</b>
• Total Families: {db.db.families.count_documents({})}

<b>Factories:</b>
• Total Factories: {db.db.factory.count_documents({})}
"""
    
    await update.message.reply_text(stats_text, parse_mode="HTML")

adminstats_handler = CommandHandler('adminstats', adminstats_command)