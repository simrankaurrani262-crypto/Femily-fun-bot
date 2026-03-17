"""
/withdraw command - Withdraw from bank
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def withdraw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Withdraw from bank"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🏦 <b>BANK WITHDRAWAL</b>\n\n"
            "Usage: /withdraw amount\n\n"
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
    
    if user['bank'] < amount:
        await update.message.reply_text(f"❌ You only have {user['bank']} 💰 in bank")
        return
    
    db.withdraw_bank(user_id, amount)
    
    updated_user = db.get_user(user_id)
    
    await update.message.reply_text(
        f"✅ <b>WITHDRAWN</b>\n\n"
        f"💳 Withdrawn {amount:,} 💰\n"
        f"Wallet: {updated_user['money']:,} 💰\n"
        f"Bank: {updated_user['bank']:,} 💰",
        parse_mode="HTML"
    )

withdraw_handler = CommandHandler('withdraw', withdraw_command)