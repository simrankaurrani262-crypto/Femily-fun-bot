"""
/account command - View account balance and info
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View account information"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    total = user['money'] + user['bank']
    rank = db.get_user_rank(user_id, 'money')
    
    account_text = f"""
<b>💳 ACCOUNT INFORMATION</b>

<b>Player:</b> @{user['username']}
<b>Level:</b> {user['level']}

<b>💰 BALANCE</b>
<b>Wallet:</b> {user['money']:,} 💰
<b>Bank:</b> {user['bank']:,} 💰
<b>Total:</b> {total:,} 💰

<b>📊 RANKING</b>
<b>Money Rank:</b> #{rank}
<b>Reputation:</b> {user['reputation']}

<b>📈 STATISTICS</b>
<b>Job:</b> {user.get('job') or 'Unemployed'}
<b>Level:</b> {user['level']}
<b>Experience:</b> {user['experience']} XP

<b>Quick Actions:</b>
/daily - Claim daily reward
/pay - Send money to player
/deposit - Add to bank
/withdraw - Get from bank
/work - Earn money from job
"""
    
    keyboard = [
        [
            InlineKeyboardButton("💰 Deposit", callback_data="account_deposit"),
            InlineKeyboardButton("💸 Withdraw", callback_data="account_withdraw"),
        ],
        [
            InlineKeyboardButton("📤 Send Money", callback_data="account_pay"),
            InlineKeyboardButton("🔄 Refresh", callback_data="account_refresh"),
        ],
    ]
    
    await update.message.reply_text(
        account_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Account viewed by {user_id}")

account_handler = CommandHandler('account', account_command)