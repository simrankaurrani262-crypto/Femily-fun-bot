"""
/orders command - View crop orders
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

ORDERS = {
    "wheat": {"buyer": "Farmer", "price": 25, "quantity": 100},
    "corn": {"buyer": "Feed Mill", "price": 40, "quantity": 50},
    "tomato": {"buyer": "Restaurant", "price": 60, "quantity": 30},
    "pumpkin": {"buyer": "Market", "price": 80, "quantity": 20},
}

async def orders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View orders"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    orders_text = "<b>📋 AVAILABLE ORDERS</b>\n\n"
    
    for crop, order in ORDERS.items():
        orders_text += f"<b>{crop.capitalize()}</b>\n"
        orders_text += f"  Buyer: {order['buyer']}\n"
        orders_text += f"  Price: {order['price']} 💰 per unit\n"
        orders_text += f"  Quantity: {order['quantity']} units\n\n"
    
    await update.message.reply_text(orders_text, parse_mode="HTML")

orders_handler = CommandHandler('orders', orders_command)