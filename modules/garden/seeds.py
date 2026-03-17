"""
/seeds command - View seed catalog
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
import logging

logger = logging.getLogger(__name__)

SEED_CATALOG = {
    "wheat": {
        "cost": 10,
        "emoji": "🌾",
        "growth_time": 3600,
        "harvest": 50,
        "description": "Fast growing crop"
    },
    "corn": {
        "cost": 20,
        "emoji": "🌽",
        "growth_time": 5400,
        "harvest": 75,
        "description": "Medium growth crop"
    },
    "carrot": {
        "cost": 15,
        "emoji": "🥕",
        "growth_time": 3600,
        "harvest": 40,
        "description": "Root vegetable"
    },
    "tomato": {
        "cost": 25,
        "emoji": "🍅",
        "growth_time": 7200,
        "harvest": 100,
        "description": "Red fruit"
    },
    "pumpkin": {
        "cost": 40,
        "emoji": "🎃",
        "growth_time": 10800,
        "harvest": 150,
        "description": "Large autumn crop"
    },
    "lettuce": {
        "cost": 12,
        "emoji": "🥬",
        "growth_time": 2700,
        "harvest": 30,
        "description": "Leafy vegetable"
    },
    "cucumber": {
        "cost": 18,
        "emoji": "🥒",
        "growth_time": 4800,
        "harvest": 60,
        "description": "Green vegetable"
    },
    "potato": {
        "cost": 22,
        "emoji": "🥔",
        "growth_time": 6300,
        "harvest": 80,
        "description": "Starchy vegetable"
    },
}

async def seeds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View seed catalog"""
    seeds_text = "<b>🌱 SEED CATALOG</b>\n\n"
    
    for seed_name, seed_info in SEED_CATALOG.items():
        seeds_text += f"{seed_info['emoji']} <b>{seed_name.capitalize()}</b>\n"
        seeds_text += f"   {seed_info['description']}\n"
        seeds_text += f"   Cost: {seed_info['cost']} 💰\n"
        seeds_text += f"   Growth Time: {seed_info['growth_time']}s\n"
        seeds_text += f"   Harvest: {seed_info['harvest']} units\n\n"
    
    keyboard = [
        [InlineKeyboardButton(f"{seed_info['emoji']} {seed_name}", 
         callback_data=f"buy_seed_{seed_name}")] 
        for seed_name in list(SEED_CATALOG.keys())[:5]
    ]
    
    await update.message.reply_text(
        seeds_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info("Seed catalog viewed")

seeds_handler = CommandHandler('seeds', seeds_command)