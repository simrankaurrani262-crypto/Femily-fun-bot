"""
/ratings command - Rate friends
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def ratings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View friend ratings"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    friends = user.get('friends', [])
    
    if not friends:
        await update.message.reply_text("❌ You have no friends to rate")
        return
    
    ratings_text = "<b>⭐ FRIEND RATINGS</b>\n\n"
    
    for friend_id in friends:
        friend = db.get_user(friend_id)
        if friend:
            # Get friend rating from database
            friend_rating = db.db.friends.find_one(
                {"user_id": user_id, "friend_id": friend_id}
            )
            rating = friend_rating.get('rating', 0) if friend_rating else 0
            
            ratings_text += f"@{friend['username']}\n"
            ratings_text += f"   Rating: {'⭐' * rating}\n"
            ratings_text += f"   Level: {friend['level']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("⭐ Rate Friend", callback_data="rate_friend")],
    ]
    
    await update.message.reply_text(
        ratings_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Ratings viewed by {user_id}")

ratings_handler = CommandHandler('ratings', ratings_command)