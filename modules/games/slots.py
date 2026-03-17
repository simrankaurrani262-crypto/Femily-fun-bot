"""
/slots command - Slot machine game
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import random
import logging

logger = logging.getLogger(__name__)

SYMBOLS = ['🍎', '🍌', '🍒', '🍓', '💎', '🔔', '⭐', '👑']

async def slots_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Play slots"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🎰 <b>SLOT MACHINE</b>\n\n"
            "Usage: /slots bet_amount\n\n"
            "Match 3 symbols to win!",
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
    
    # Spin slots
    db.withdraw_money(user_id, bet)
    
    reel1 = random.choice(SYMBOLS)
    reel2 = random.choice(SYMBOLS)
    reel3 = random.choice(SYMBOLS)
    
    slots_text = f"""
<b>🎰 SLOT MACHINE</b>

{reel1} {reel2} {reel3}

Bet: {bet} 💰
"""
    
    if reel1 == reel2 == reel3:
        # JACKPOT!
        winnings = bet * 50
        db.add_money(user_id, winnings)
        
        slots_text += f"\n🎉 <b>JACKPOT!!!</b>\n"
        slots_text += f"💰 Won: {winnings:,} 💰"
        logger.info(f"Slots jackpot: {user_id} won {winnings}")
    elif reel1 == reel2 or reel2 == reel3 or reel1 == reel3:
        # Two match
        winnings = bet * 3
        db.add_money(user_id, winnings)
        
        slots_text += f"\n🎊 <b>YOU WON!</b>\n"
        slots_text += f"💰 Won: {winnings:,} 💰"
    else:
        slots_text += f"\n😢 <b>LOST</b>\n"
        slots_text += f"Better luck next time!"
    
    await update.message.reply_text(slots_text, parse_mode="HTML")
    logger.info(f"Slots: {user_id} bet {bet}")

slots_handler = CommandHandler('slots', slots_command)