"""
/harvest command - Harvest crops
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def harvest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Harvest crops"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    garden = user.get('garden', {})
    plots = garden.get('plots', [])
    
    if not plots:
        await update.message.reply_text("❌ You have no crops to harvest")
        return
    
    harvest_text = "<b>🌾 HARVEST READY</b>\n\n"
    total_harvest = 0
    
    for idx, plot in enumerate(plots, 1):
        if plot.get('growth', 0) >= 100:
            harvest_text += f"{idx}. {plot['crop']} - Ready! ✅\n"
            total_harvest += 100
    
    if total_harvest == 0:
        await update.message.reply_text("❌ No crops are ready to harvest yet")
        return
    
    # Harvest all ready crops
    ready_plots = [p for p in plots if p.get('growth', 0) >= 100]
    remaining_plots = [p for p in plots if p.get('growth', 0) < 100]
    
    for plot in ready_plots:
        db.add_item(user_id, plot['crop'])
    
    db.update_user(user_id, {'garden.plots': remaining_plots})
    
    harvest_text += f"\n✅ Harvested {len(ready_plots)} crops!"
    await update.message.reply_text(harvest_text, parse_mode="HTML")
    logger.info(f"Harvest: {user_id} harvested {len(ready_plots)} crops")

harvest_handler = CommandHandler('harvest', harvest_command)