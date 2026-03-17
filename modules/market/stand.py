"""
/stand command - View your market stand
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def stand_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View your stand"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    market = db.db.market.find_one({"user_id": user_id})
    
    if not market:
        db.db.market.insert_one({
            "user_id": user_id,
            "items_for_sale": [],
            "total_sold": 0,
            "revenue": 0
        })
        market = db.db.market.find_one({"user_id": user_id})
    
    stand_text = f"""
<b>🛒 YOUR MARKET STAND</b>

<b>Items for Sale:</b> {len(market.get('items_for_sale', []))}
<b>Total Sold:</b> {market.get('total_sold', 0)}
<b>Revenue:</b> {market.get('revenue', 0):,} 💰

@{user['username']}'s Stand
"""
    
    keyboard = [
        [InlineKeyboardButton("📝 Put Item", callback_data="market_put")],
        [InlineKeyboardButton("🔍 Browse", callback_data="market_browse")],
    ]
    
    await update.message.reply_text(
        stand_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

stand_handler = CommandHandler('stand', stand_command)