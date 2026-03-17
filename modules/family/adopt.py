"""
/adopt command - Adopt someone
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def adopt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adopt command"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    family = db.get_family(user_id)
    
    if len(family.get('children', [])) >= 10:
        await update.message.reply_text("❌ You have reached the maximum children limit (10)")
        return
    
    if not context.args:
        await update.message.reply_text(
            "👶 <b>ADOPTION</b>\n\n"
            "Usage: /adopt @username\n\n"
            "Adopt someone as your child.\n"
            "They will receive an adoption notification.",
            parse_mode="HTML"
        )
        return
    
    target_username = context.args[0].lstrip('@')
    target = db.db.users.find_one({"username": target_username})
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target['user_id'] == user_id:
        await update.message.reply_text("❌ You can't adopt yourself!")
        return
    
    target_family = db.get_family(target['user_id'])
    if target_family.get('parents'):
        await update.message.reply_text(f"❌ @{target['username']} already has parents")
        return
    
    # Add child
    db.add_child(user_id, target['user_id'])
    
    await update.message.reply_text(
        f"👶 <b>ADOPTION COMPLETE!</b>\n\n"
        f"@{target['username']} is now your child!\n\n"
        f"View your family tree with /tree",
        parse_mode="HTML"
    )
    
    logger.info(f"Adoption: {user_id} adopted {target['user_id']}")

adopt_handler = CommandHandler('adopt', adopt_command)