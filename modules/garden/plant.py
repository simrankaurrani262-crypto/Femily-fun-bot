"""
/plant command - Plant crops
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

CROPS = {
    "wheat": {"time": 3600, "harvest": 50, "cost": 10, "emoji": "🌾"},
    "corn": {"time": 5400, "harvest": 75, "cost": 20, "emoji": "🌽"},
    "carrot": {"time": 3600, "harvest": 40, "cost": 15, "emoji": "🥕"},
    "tomato": {"time": 7200, "harvest": 100, "cost": 25, "emoji": "🍅"},
    "pumpkin": {"time": 10800, "harvest": 150, "cost": 40, "emoji": "🎃"},
}

async def plant_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Plant a crop"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        plant_text = "<b>🌱 PLANT CROPS</b>\n\n"
        for crop_name, crop_info in CROPS.items():
            plant_text += f"{crop_info['emoji']} {crop_name.capitalize()}\n"
            plant_text += f"   Time: {crop_info['time']}s\n"
            plant_text += f"   Harvest: {crop_info['harvest']} units\n"
            plant_text += f"   Cost: {crop_info['cost']} 💰\n\n"
        
        await update.message.reply_text(plant_text, parse_mode="HTML")
        return
    
    crop_name = context.args[0].lower()
    
    if crop_name not in CROPS:
        await update.message.reply_text("❌ Crop not found")
        return
    
    crop_info = CROPS[crop_name]
    
    if user['money'] < crop_info['cost']:
        await update.message.reply_text(f"❌ You need {crop_info['cost']} 💰")
        return
    
    # Plant crop
    db.withdraw_money(user_id, crop_info['cost'])
    
    garden = user.get('garden', {})
    plots = garden.get('plots', [])
    
    plots.append({
        "crop": crop_name,
        "growth": 0,
        "planted_at": db.db.time.time() if hasattr(db.db, 'time') else 0
    })
    
    db.update_user(user_id, {'garden.plots': plots})
    
    await update.message.reply_text(
        f"✅ <b>CROP PLANTED!</b>\n\n"
        f"{crop_info['emoji']} {crop_name.capitalize()}\n"
        f"⏱️ Growth time: {crop_info['time']}s\n"
        f"💰 Cost: {crop_info['cost']}",
        parse_mode="HTML"
    )
    logger.info(f"Crop planted: {user_id} planted {crop_name}")

plant_handler = CommandHandler('plant', plant_command)