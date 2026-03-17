"""
/lottery command - Lottery game
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
from modules.utils.cooldown import CooldownManager
import random
import logging

logger = logging.getLogger(__name__)

async def lottery_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lottery game"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🎰 <b>LOTTERY</b>\n\n"
            "Usage: /lottery amount\n\n"
            "Jackpot: 1000x your bet!\n"
            "Good luck!",
            parse_mode="HTML"
        )
        return
    
    try:
        bet = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid amount")
        return
    
    if bet <= 0:
        await update.message.reply_text("❌ Bet must be positive")
        return
    
    if user['money'] < bet:
        await update.message.reply_text(f"❌ You only have {user['money']} 💰")
        return
    
    # Draw lottery
    db.withdraw_money(user_id, bet)
    
    result = random.randint(1, 1000)
    
    if result == 1:
        # JACKPOT!
        winnings = bet * 1000
        db.add_money(user_id, winnings)
        
        await update.message.reply_text(
            f"🎉 <b>JACKPOT!!!</b>\n\n"
            f"🎰 Number: {result}\n"
            f"💰 Won: {winnings:,} 💰\n"
            f"Balance: {user['money'] - bet + winnings:,} 💰",
            parse_mode="HTML"
        )
        logger.info(f"Lottery jackpot: {user_id} won {winnings}")
    elif result <= 10:
        # Big win
        winnings = bet * 100
        db.add_money(user_id, winnings)
        
        await update.message.reply_text(
            f"🎊 <b>BIG WIN!</b>\n\n"
            f"🎰 Number: {result}\n"
            f"💰 Won: {winnings:,} 💰",
            parse_mode="HTML"
        )
    elif result <= 50:
        # Small win
        winnings = bet * 5
        db.add_money(user_id, winnings)
        
        await update.message.reply_text(
            f"🎉 <b>YOU WON!</b>\n\n"
            f"🎰 Number: {result}\n"
            f"💰 Won: {winnings:,} 💰",
            parse_mode="HTML"
        )
    else:
        # Lost
        await update.message.reply_text(
            f"😢 <b>YOU LOST</b>\n\n"
            f"🎰 Number: {result}\n"
            f"Better luck next time!"
        )
    
    logger.info(f"Lottery: {user_id} bet {bet}, result {result}")

lottery_handler = CommandHandler('lottery', lottery_command)