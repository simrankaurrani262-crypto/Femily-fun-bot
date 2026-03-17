"""
/pay command - Transfer money to another player
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def pay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pay another player"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "💳 <b>PAYMENT</b>\n\n"
            "Usage: /pay @username amount\n\n"
            "Example: /pay @friend 100",
            parse_mode="HTML"
        )
        return
    
    target_username = context.args[0].lstrip('@')
    target = db.db.users.find_one({"username": target_username})
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target['user_id'] == user_id:
        await update.message.reply_text("❌ You can't pay yourself!")
        return
    
    try:
        amount = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Invalid amount")
        return
    
    if amount <= 0:
        await update.message.reply_text("❌ Amount must be positive")
        return
    
    if user['money'] < amount:
        await update.message.reply_text(f"❌ You only have {user['money']} 💰")
        return
    
    # Transfer money
    db.withdraw_money(user_id, amount)
    db.add_money(target['user_id'], amount)
    
    await update.message.reply_text(
        f"✅ <b>PAYMENT SENT</b>\n\n"
        f"💳 Sent {amount:,} 💰 to @{target['username']}\n"
        f"Your balance: {user['money'] - amount:,} 💰",
        parse_mode="HTML"
    )
    
    logger.info(f"Payment: {user_id} paid {target['user_id']} {amount}")

pay_handler = CommandHandler('pay', pay_command)