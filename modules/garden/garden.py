"""
/garden command - View garden
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def garden_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View garden"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    garden = user.get('garden', {})
    plots = garden.get('plots', [])
    barn = garden.get('barn', [])
    
    garden_text = f"""
<b>🌾 YOUR GARDEN</b>

<b>Plots:</b> {len(plots)} plots
<b>Barn Storage:</b> {len(barn)} items

<b>Crops Growing:</b>
"""
    
    for idx, plot in enumerate(plots, 1):
        garden_text += f"{idx}. {plot.get('crop', 'Empty')} - {plot.get('growth', 0)}%\n"
    
    keyboard = [
        [
            InlineKeyboardButton("🌱 Plant", callback_data="garden_plant"),
            InlineKeyboardButton("🌾 Harvest", callback_data="garden_harvest"),
        ],
        [
            InlineKeyboardButton("🥗 Barn", callback_data="garden_barn"),
            InlineKeyboardButton("✨ Fertilise", callback_data="garden_fertilise"),
        ],
    ]
    
    await update.message.reply_text(
        garden_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

garden_handler = CommandHandler('garden', garden_command)