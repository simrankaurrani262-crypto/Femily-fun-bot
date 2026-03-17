"""
/bid command - Bid on auction
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def bid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bid on auction"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "💰 <b>BID ON AUCTION</b>\n\n"
            "Usage: /bid auction_id amount\n\n"
            "Example: /bid 1 500",
            parse_mode="HTML"
        )
        return
    
    try:
        auction_id = int(context.args[0])
        bid_amount = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Invalid input")
        return
    
    if user['money'] < bid_amount:
        await update.message.reply_text(f"❌ You need {bid_amount} 💰")
        return
    
    # Place bid
    db.withdraw_money(user_id, bid_amount)
    
    await update.message.reply_text(
        f"✅ <b>BID PLACED!</b>\n\n"
        f"💰 Amount: {bid_amount}\n"
        f"Your balance: {user['money'] - bid_amount:,} 💰",
        parse_mode="HTML"
    )

bid_handler = CommandHandler('bid', bid_command)