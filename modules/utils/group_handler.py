"""
Shared logic for group commands (reply-to support)
"""
from telegram import Update
from telegram.ext import ContextTypes
from database import db
import logging

logger = logging.getLogger(__name__)

def get_display_name(user):
    """Get display name for user"""
    if user.get('first_name'):
        return user['first_name']
    elif user.get('username'):
        return f"@{user['username']}"
    else:
        return f"user{user['user_id']}"

async def get_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Extract target user from:
    1. reply_to_message.from_user (if replying to someone)
    2. context.args[0] as @username (fallback)
    
    Returns: (target_user_id, target_name, error_message)
    """
    # Check if replying to a message
    if update.message.reply_to_message:
        target_user_id = update.message.reply_to_message.from_user.id
        target_name = (
            update.message.reply_to_message.from_user.first_name or
            update.message.reply_to_message.from_user.username or
            f"user{target_user_id}"
        )
        return target_user_id, target_name, None
    
    # Fall back to @username argument
    if not context.args:
        return None, None, "Reply to a user or use /command @username"
    
    target_username = context.args[0].lstrip('@')
    target_user = db.db.users.find_one({"username": target_username})
    
    if not target_user:
        return None, None, f"❌ User @{target_username} not found"
    
    target_user_id = target_user['user_id']
    target_name = get_display_name(target_user)
    
    return target_user_id, target_name, None
