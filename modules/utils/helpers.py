"""
Helper functions for bot
"""
from database import db
from config import ERRORS, SUCCESS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logger = logging.getLogger(__name__)

def ensure_user_registered(user_id):
    """Ensure user exists, create if not"""
    user = db.get_user(user_id)
    return user is not None

def create_user_if_needed(user_id, username, first_name):
    """Create user if not exists"""
    if not db.get_user(user_id):
        return db.create_user(user_id, username, first_name)
    return db.get_user(user_id)

def format_money(amount):
    """Format money with commas"""
    return f"{amount:,}💰"

def create_confirm_keyboard(yes_callback, no_callback):
    """Create yes/no confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes", callback_data=yes_callback),
            InlineKeyboardButton("❌ No", callback_data=no_callback)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_pagination_keyboard(page, total_pages, callback_prefix):
    """Create pagination keyboard"""
    keyboard = []
    
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"{callback_prefix}_page_{page-1}"))
    
    buttons.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="noop"))
    
    if page < total_pages:
        buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"{callback_prefix}_page_{page+1}"))
    
    keyboard.append(buttons)
    return InlineKeyboardMarkup(keyboard)

def get_user_brief(user_id):
    """Get brief user info"""
    user = db.get_user(user_id)
    if not user:
        return "Unknown User"
    return f"<b>{user['username']}</b>\nLevel {user['level']} | {format_money(user['money'])}"