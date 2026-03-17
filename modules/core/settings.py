"""
/settings command handler
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings menu"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    keyboard = [
        [InlineKeyboardButton("🔔 Notifications", callback_data="settings_notifications")],
        [InlineKeyboardButton("🎨 Theme", callback_data="settings_theme")],
        [InlineKeyboardButton("🔒 Privacy", callback_data="settings_privacy")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
    ]
    
    await update.message.reply_text(
        "<b>⚙️ SETTINGS</b>\n\nChoose a setting to adjust:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

settings_handler = CommandHandler('settings', settings_command)
