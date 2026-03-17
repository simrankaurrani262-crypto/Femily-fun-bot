"""
/deposit command - Deposit to bank
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def deposit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Deposit to bank"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🏦 <b>BANK DEPOSIT</b>\n\n"
            "Usage: /deposit amount\n\n"
            f"Your wallet: {user['money']:,} 💰\n"
            f"Your bank: {user['bank']:,} 💰",
            parse_mode="HTML"
        )
        return
    
    try:
        amount = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid amount")
        return
    
    if amount <= 0:
        await update.message.reply_text("❌ Amount must be positive")
        return
    
    if user['money'] < amount:
        await update.message.reply_text(f"❌ You only have {user['money']} 💰")
        return
    
    db.add_bank(user_id, amount)
    
    updated_user = db.get_user(user_id)
    
    await update.message.reply_text(
        f"✅ <b>DEPOSITED</b>\n\n"
        f"💳 Deposited {amount:,} 💰\n"
        f"Wallet: {updated_user['money']:,} 💰\n"
        f"Bank: {updated_user['bank']:,} 💰",
        parse_mode="HTML"
    )

deposit_handler = CommandHandler('deposit', deposit_command)