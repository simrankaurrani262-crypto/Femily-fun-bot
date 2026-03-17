"""
/dice command - Dice game
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import random
import logging

logger = logging.getLogger(__name__)

async def dice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Play dice game"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "🎲 <b>DICE GAME</b>\n\n"
            "Usage: /dice bet_amount guess(1-6)\n\n"
            "Example: /dice 100 6",
            parse_mode="HTML"
        )
        return
    
    try:
        bet = int(context.args[0])
        guess = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Invalid input")
        return
    
    if guess < 1 or guess > 6:
        await update.message.reply_text("❌ Guess must be 1-6")
        return
    
    if user['money'] < bet:
        await update.message.reply_text(f"❌ You only have {user['money']} 💰")
        return
    
    # Roll dice
    db.withdraw_money(user_id, bet)
    
    roll = random.randint(1, 6)
    
    dice_text = f"""
<b>🎲 DICE GAME</b>

Your Guess: {guess}
🎲 Result: {roll}

Bet: {bet} 💰
"""
    
    if roll == guess:
        # Won!
        winnings = bet * 5
        db.add_money(user_id, winnings)
        
        dice_text += f"\n✅ <b>YOU WON!</b>\n"
        dice_text += f"💰 Won: {winnings:,} 💰"
        logger.info(f"Dice: {user_id} won {winnings}")
    else:
        dice_text += f"\n❌ <b>LOST</b>\n"
        dice_text += f"Better luck next time!"
    
    await update.message.reply_text(dice_text, parse_mode="HTML")

dice_handler = CommandHandler('dice', dice_command)