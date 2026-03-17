"""
/auction command - View auctions
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def auction_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View auctions"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    # Get active auctions
    auctions = list(db.db.market.find({"type": "auction"}).limit(10))
    
    if not auctions:
        await update.message.reply_text("❌ No active auctions")
        return
    
    auction_text = "<b>🔨 ACTIVE AUCTIONS</b>\n\n"
    
    for idx, auction in enumerate(auctions, 1):
        seller = db.get_user(auction['user_id'])
        auction_text += f"{idx}. {auction['item']}\n"
        auction_text += f"   Current Bid: {auction.get('current_bid', 0)} 💰\n"
        auction_text += f"   Seller: @{seller['username']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("📝 Place Bid", callback_data="auction_bid")],
    ]
    
    await update.message.reply_text(
        auction_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

auction_handler = CommandHandler('auction', auction_command)