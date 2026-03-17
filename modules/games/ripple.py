"""
/ripple command - Ripple game
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import random
import logging

logger = logging.getLogger(__name__)

async def ripple_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ripple game"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🌊 <b>RIPPLE GAME</b>\n\n"
            "Usage: /ripple bet_amount\n\n"
            "Watch the ripple!",
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
    
    db.withdraw_money(user_id, bet)
    
    # Ripple effect
    multiplier = random.uniform(0.5, 5.0)
    winnings = int(bet * multiplier)
    
    if multiplier > 1:
        db.add_money(user_id, winnings)
        await update.message.reply_text(
            f"🌊 <b>RIPPLE!</b>\n\n"
            f"Multiplier: {multiplier:.2f}x\n"
            f"💰 Won: {winnings:,} 💰"
        )
    else:
        await update.message.reply_text(
            f"🌊 <b>RIPPLE</b>\n\n"
            f"Multiplier: {multiplier:.2f}x\n"
            f"❌ You lost"
        )

ripple_handler = CommandHandler('ripple', ripple_command)