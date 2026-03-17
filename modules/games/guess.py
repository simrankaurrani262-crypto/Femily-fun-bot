"""
/guess command - Number guessing game
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import db
import random
import logging

logger = logging.getLogger(__name__)

async def guess_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Number guessing game"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🎯 <b>NUMBER GUESSING GAME</b>\n\n"
            "Usage: /guess bet_amount\n\n"
            "Guess a number between 1-100!\n"
            "Get it right to win 10x your bet!",
            parse_mode="HTML"
        )
        return
    
    try:
        bet = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid bet")
        return
    
    if user['money'] < bet:
        await update.message.reply_text(f"❌ You only have {user['money']} 💰")
        return
    
    # Generate number
    target_number = random.randint(1, 100)
    
    context.user_data['guess_game'] = {
        'target': target_number,
        'bet': bet,
        'user_id': user_id
    }
    
    db.withdraw_money(user_id, bet)
    
    guess_text = """
<b>🎯 GUESS THE NUMBER</b>

I'm thinking of a number between 1-100...
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔢 Enter Guess", callback_data="guess_enter"),
        ],
    ]
    
    await update.message.reply_text(
        guess_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

guess_handler = CommandHandler('guess', guess_command)