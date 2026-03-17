"""
/stands command - View all market stands
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def stands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all stands"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    # Get all market stands
    all_stands = list(db.db.market.find({}, {"user_id": 1, "revenue": 1, "total_sold": 1}).limit(10))
    
    stands_text = "<b>🛒 MARKET STANDS</b>\n\n"
    
    for idx, stand in enumerate(all_stands, 1):
        seller = db.get_user(stand['user_id'])
        if seller:
            stands_text += f"{idx}. @{seller['username']}\n"
            stands_text += f"   Revenue: {stand.get('revenue', 0):,} 💰\n"
            stands_text += f"   Sold: {stand.get('total_sold', 0)}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔍 Browse Stands", callback_data="market_browse_all")],
    ]
    
    await update.message.reply_text(
        stands_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

stands_handler = CommandHandler('stands', stands_command)