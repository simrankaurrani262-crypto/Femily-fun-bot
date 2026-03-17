"""
/familyboard command - Family leaderboard
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

def get_display_name(user):
    """Get display name for user - prefer first_name, then username, then fallback"""
    if user.get('first_name'):
        return user['first_name']
    elif user.get('username'):
        return f"@{user['username']}"
    else:
        return f"user{user['user_id']}"

async def familyboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Family leaderboard"""
    user_id = update.effective_user.id
    
    # Get families by size
    families = []
    for family in db.db.families.find():
        family_size = (
            len(family.get('children', [])) +
            len(family.get('parents', [])) +
            len(family.get('grandchildren', [])) +
            len(family.get('siblings', [])) +
            (1 if family.get('partner') else 0) + 1
        )
        families.append({
            'user_id': family['user_id'],
            'size': family_size
        })
    
    # Sort by size
    families.sort(key=lambda x: x['size'], reverse=True)
    
    board_text = "<b>👨‍👩‍👧‍👦 FAMILY LEADERBOARD</b>\n\n"
    
    for idx, fam in enumerate(families[:10], 1):
        user = db.get_user(fam['user_id'])
        if user:
            display_name = get_display_name(user)
            board_text += f"{idx}. {display_name} - {fam['size']} members\n"
    
    await update.message.reply_text(board_text, parse_mode="HTML")
    logger.info(f"Family board viewed by {user_id}")

familyboard_handler = CommandHandler('familyboard', familyboard_command)
