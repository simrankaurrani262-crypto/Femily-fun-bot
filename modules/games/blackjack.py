"""
/blackjack command - Blackjack game
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import db
import random
import logging

logger = logging.getLogger(__name__)

CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def card_value(card):
    """Get card value"""
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)

def hand_value(cards):
    """Calculate hand value"""
    value = sum(card_value(c) for c in cards)
    aces = cards.count('A')
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value

async def blackjack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Play blackjack"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🎰 <b>BLACKJACK</b>\n\n"
            "Usage: /blackjack bet_amount\n\n"
            "Try to get 21 without going over!",
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
    
    # Deal cards
    player_hand = [random.choice(CARDS), random.choice(CARDS)]
    dealer_hand = [random.choice(CARDS), random.choice(CARDS)]
    
    player_value = hand_value(player_hand)
    dealer_value = hand_value(dealer_hand)
    
    # Store game state
    context.user_data['blackjack'] = {
        'bet': bet,
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'user_id': user_id
    }
    
    bj_text = f"""
<b>🎰 BLACKJACK</b>

<b>Your Hand:</b> {' '.join(player_hand)} = {player_value}
<b>Dealer:</b> {dealer_hand[0]} ?

<b>Bet:</b> {bet} 💰
"""
    
    keyboard = [
        [
            InlineKeyboardButton("📍 Hit", callback_data="bj_hit"),
            InlineKeyboardButton("⏹️ Stand", callback_data="bj_stand"),
        ],
    ]
    
    await update.message.reply_text(
        bj_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

blackjack_handler = CommandHandler('blackjack', blackjack_command)