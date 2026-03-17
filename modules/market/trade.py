"""
/trade command - Trade with others
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trade with someone"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if len(context.args) < 3:
        await update.message.reply_text(
            "💱 <b>TRADE</b>\n\n"
            "Usage: /trade @username item amount\n\n"
            "Example: /trade @friend wheat 50",
            parse_mode="HTML"
        )
        return
    
    target_username = context.args[0].lstrip('@')
    item_name = context.args[1].lower()
    
    try:
        amount = int(context.args[2])
    except ValueError:
        await update.message.reply_text("❌ Invalid amount")
        return
    
    target = db.db.users.find_one({"username": target_username})
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    # Check if user has item
    if user.get('inventory', {}).get(item_name, 0) < amount:
        await update.message.reply_text(f"❌ You don't have {amount} {item_name}")
        return
    
    # Trade
    db.remove_item(user_id, item_name, amount)
    db.add_item(target['user_id'], item_name, amount)
    
    await update.message.reply_text(
        f"✅ <b>TRADE COMPLETED!</b>\n\n"
        f"Sent {amount} {item_name} to @{target['username']}",
        parse_mode="HTML"
    )
    logger.info(f"Trade: {user_id} traded {amount} {item_name} to {target['user_id']}")

trade_handler = CommandHandler('trade', trade_command)