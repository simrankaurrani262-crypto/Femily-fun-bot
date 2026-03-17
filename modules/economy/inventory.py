"""
/inventory command - View inventory
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def inventory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View inventory"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    inventory = user.get('inventory', {})
    
    if not inventory:
        await update.message.reply_text("📦 Your inventory is empty")
        return
    
    inv_text = "<b>📦 INVENTORY</b>\n\n"
    for item, quantity in inventory.items():
        inv_text += f"• {item} x{quantity}\n"
    
    await update.message.reply_text(inv_text, parse_mode="HTML")
    logger.info(f"Inventory viewed by {user_id}")

inventory_handler = CommandHandler('inventory', inventory_command)