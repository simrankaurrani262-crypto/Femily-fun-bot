"""
/weapon and /buyweapon commands
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

WEAPONS = {
    "knife": {"cost": 100, "power": 5, "emoji": "🔪"},
    "sword": {"cost": 250, "power": 15, "emoji": "⚔️"},
    "rifle": {"cost": 500, "power": 30, "emoji": "🔫"},
    "bomb": {"cost": 1000, "power": 50, "emoji": "💣"},
    "laser": {"cost": 2000, "power": 100, "emoji": "🔫"},
}

async def weapon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View weapons"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    weapons_text = "<b>⚔️ WEAPONS SHOP</b>\n\n"
    
    for weapon_name, weapon_info in WEAPONS.items():
        weapons_text += f"{weapon_info['emoji']} {weapon_name.capitalize()}\n"
        weapons_text += f"   Cost: {weapon_info['cost']} 💰\n"
        weapons_text += f"   Power: +{weapon_info['power']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton(f"{weapon_info['emoji']} {weapon_name}", callback_data=f"buy_weapon_{weapon_name}")]
        for weapon_name, weapon_info in WEAPONS.items()
    ]
    
    await update.message.reply_text(
        weapons_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buyweapon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buy a weapon"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "⚔️ <b>BUY WEAPON</b>\n\n"
            "Usage: /buyweapon weapon_name\n\n"
            "Available: knife, sword, rifle, bomb, laser",
            parse_mode="HTML"
        )
        return
    
    weapon_name = context.args[0].lower()
    
    if weapon_name not in WEAPONS:
        await update.message.reply_text(f"❌ Weapon '{weapon_name}' not found")
        return
    
    weapon_info = WEAPONS[weapon_name]
    
    if user['money'] < weapon_info['cost']:
        await update.message.reply_text(f"❌ You need {weapon_info['cost']} 💰")
        return
    
    # Buy weapon
    db.withdraw_money(user_id, weapon_info['cost'])
    db.add_item(user_id, weapon_name)
    
    await update.message.reply_text(
        f"✅ <b>WEAPON PURCHASED!</b>\n\n"
        f"{weapon_info['emoji']} {weapon_name.capitalize()}\n"
        f"Power: +{weapon_info['power']}\n"
        f"Cost: {weapon_info['cost']} 💰",
        parse_mode="HTML"
    )
    logger.info(f"Weapon purchased: {user_id} bought {weapon_name}")

weapon_handler = CommandHandler('weapon', weapon_command)
buyweapon_handler = CommandHandler('buyweapon', buyweapon_command)