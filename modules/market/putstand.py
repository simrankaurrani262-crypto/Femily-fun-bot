"""
/putstand command - Put item on market stand
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def putstand_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Put item on stand"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if len(context.args) < 3:
        await update.message.reply_text(
            "📝 <b>PUT ITEM ON STAND</b>\n\n"
            "Usage: /putstand item_name quantity price\n\n"
            "Example: /putstand wheat 50 20",
            parse_mode="HTML"
        )
        return
    
    item_name = context.args[0].lower()
    try:
        quantity = int(context.args[1])
        price = int(context.args[2])
    except ValueError:
        await update.message.reply_text("❌ Invalid quantity or price")
        return
    
    # Check if user has item
    if user.get('inventory', {}).get(item_name, 0) < quantity:
        await update.message.reply_text(f"❌ You don't have {quantity} {item_name}")
        return
    
    # Remove from inventory
    db.remove_item(user_id, item_name, quantity)
    
    # Add to market stand
    market = db.db.market.find_one({"user_id": user_id})
    if market:
        db.db.market.update_one(
            {"user_id": user_id},
            {"$push": {"items_for_sale": {
                "item": item_name,
                "quantity": quantity,
                "price": price,
                "listed_at": db.db.time.time() if hasattr(db.db, 'time') else 0
            }}}
        )
    else:
        db.db.market.insert_one({
            "user_id": user_id,
            "items_for_sale": [{
                "item": item_name,
                "quantity": quantity,
                "price": price,
                "listed_at": db.db.time.time() if hasattr(db.db, 'time') else 0
            }],
            "total_sold": 0,
            "revenue": 0
        })
    
    await update.message.reply_text(
        f"✅ <b>ITEM LISTED!</b>\n\n"
        f"Item: {item_name}\n"
        f"Quantity: {quantity}\n"
        f"Price: {price} 💰 each\n"
        f"Total: {quantity * price} 💰",
        parse_mode="HTML"
    )
    logger.info(f"Item listed: {user_id} listed {quantity} {item_name} for {price} each")

putstand_handler = CommandHandler('putstand', putstand_command)