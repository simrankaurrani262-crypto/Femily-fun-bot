"""
/disown command - Disown a child
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def disown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Disown a child"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "⚠️ <b>DISOWN</b>\n\n"
            "Usage: /disown @username\n\n"
            "<i>This action cannot be undone!</i>",
            parse_mode="HTML"
        )
        return
    
    target_username = context.args[0].lstrip('@')
    target = db.db.users.find_one({"username": target_username})
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    family = db.get_family(user_id)
    
    if target['user_id'] not in family.get('children', []):
        await update.message.reply_text(f"❌ @{target['username']} is not your child")
        return
    
    # Remove child
    db.db.families.update_one(
        {"user_id": user_id},
        {"$pull": {"children": target['user_id']}}
    )
    
    db.db.families.update_one(
        {"user_id": target['user_id']},
        {"$pull": {"parents": user_id}}
    )
    
    await update.message.reply_text(
        f"⚠️ <b>DISOWNED</b>\n\n"
        f"@{target['username']} is no longer your child.",
        parse_mode="HTML"
    )
    
    logger.info(f"Disown: {user_id} disowned {target['user_id']}")

disown_handler = CommandHandler('disown', disown_command)