"""
/shop and /buy commands - Item shop system
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

SHOP_ITEMS = {
    "apple": {"price": 10, "emoji": "🍎", "description": "Healthy snack"},
    "banana": {"price": 15, "emoji": "🍌", "description": "Energy food"},
    "orange": {"price": 12, "emoji": "🍊", "description": "Vitamin C boost"},
    "sword": {"price": 250, "emoji": "⚔️", "description": "Combat weapon"},
    "shield": {"price": 150, "emoji": "🛡️", "description": "Defense armor"},
    "potion": {"price": 50, "emoji": "🧪", "description": "Health restoration"},
    "medicine": {"price": 100, "emoji": "💊", "description": "Healing item"},
    "seed": {"price": 5, "emoji": "🌱", "description": "Plant seed"},
    "fertilizer": {"price": 25, "emoji": "🧬", "description": "Plant growth"},
    "scroll": {"price": 75, "emoji": "📜", "description": "Ancient wisdom"},
    "ring": {"price": 500, "emoji": "💍", "description": "Lucky accessory"},
    "crown": {"price": 1000, "emoji": "👑", "description": "Royal item"},
}

async def shop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View shop"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    shop_text = "<b>🛒 ITEM SHOP</b>\n\n"
    
    for item_name, item_info in SHOP_ITEMS.items():
        shop_text += f"{item_info['emoji']} <b>{item_name.capitalize()}</b>\n"
        shop_text += f"   {item_info['description']}\n"
        shop_text += f"   Price: {item_info['price']} 💰\n\n"
    
    keyboard = [
        [InlineKeyboardButton(f"{SHOP_ITEMS[item]['emoji']} {item}", 
         callback_data=f"buy_{item}")] 
        for item in list(SHOP_ITEMS.keys())
    ]
    
    await update.message.reply_text(
        shop_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Shop viewed by {user_id}")

async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buy item"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🛒 <b>BUY ITEM</b>\n\n"
            "Usage: /buy item_name\n\n"
            "Available items:\n" + 
            "\n".join([f"• {name}" for name in SHOP_ITEMS.keys()]),
            parse_mode="HTML"
        )
        return
    
    item_name = context.args[0].lower()
    
    if item_name not in SHOP_ITEMS:
        await update.message.reply_text("❌ Item not found in shop")
        return
    
    item_info = SHOP_ITEMS[item_name]
    
    if user['money'] < item_info['price']:
        await update.message.reply_text(
            f"❌ You need {item_info['price']} 💰\n"
            f"Your balance: {user['money']} 💰"
        )
        return
    
    # Purchase item
    db.withdraw_money(user_id, item_info['price'])
    db.add_item(user_id, item_name)
    
    await update.message.reply_text(
        f"✅ <b>PURCHASE SUCCESSFUL!</b>\n\n"
        f"{item_info['emoji']} {item_name.capitalize()}\n"
        f"Cost: {item_info['price']} 💰\n"
        f"Balance: {user['money'] - item_info['price']:,} 💰",
        parse_mode="HTML"
    )
    logger.info(f"Purchase: {user_id} bought {item_name} for {item_info['price']}")

shop_handler = CommandHandler('shop', shop_command)
buy_handler = CommandHandler('buy', buy_command)