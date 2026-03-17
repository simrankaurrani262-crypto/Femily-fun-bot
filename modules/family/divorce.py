"""
/divorce command - Divorce
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def divorce_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Divorce command"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    family = db.get_family(user_id)
    
    if not family.get('partner'):
        await update.message.reply_text("❌ You are not married")
        return
    
    partner_id = family['partner']
    partner = db.get_user(partner_id)
    
    db.remove_partner(user_id)
    
    await update.message.reply_text(
        f"😢 <b>DIVORCE</b>\n\n"
        f"You have divorced @{partner['username']}\n\n"
        f"You can now marry someone else.",
        parse_mode="HTML"
    )
    
    logger.info(f"Divorce: {user_id} divorced {partner_id}")

divorce_handler = CommandHandler('divorce', divorce_command)