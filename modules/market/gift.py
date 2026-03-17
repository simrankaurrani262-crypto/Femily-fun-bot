"""
/gift command - Gift to someone
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def gift_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gift to someone"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "🎁 <b>GIFT</b>\n\n"
            "Usage: /gift @username item\n\n"
            "Example: /gift @friend apple",
            parse_mode="HTML"
        )
        return
    
    target_username = context.args[0].lstrip('@')
    item_name = context.args[1].lower()
    
    target = db.db.users.find_one({"username": target_username})
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if user.get('inventory', {}).get(item_name, 0) < 1:
        await update.message.reply_text(f"❌ You don't have {item_name}")
        return
    
    # Gift
    db.remove_item(user_id, item_name)
    db.add_item(target['user_id'], item_name)
    
    await update.message.reply_text(
        f"✅ <b>GIFT SENT!</b>\n\n"
        f"🎁 Gifted {item_name} to @{target['username']}",
        parse_mode="HTML"
    )

gift_handler = CommandHandler('gift', gift_command)