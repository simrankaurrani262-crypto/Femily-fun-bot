"""
/bank command - Advanced bank operations
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def bank_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View bank info"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    # Calculate interest
    monthly_interest = user['bank'] * 0.02
    
    bank_text = f"""
<b>🏦 BANK INFORMATION</b>

<b>Your Account:</b>
  Balance: {user['bank']:,} 💰
  Interest Rate: 2% per month
  Monthly Interest: {monthly_interest:.0f} 💰
  
<b>Account Type:</b> {('Premium' if user['bank'] > 5000 else 'Standard')}

<b>Services:</b>
  • Deposit money: /deposit amount
  • Withdraw money: /withdraw amount
  • Take loan: /loan amount
  • Repay loan: /repay amount
  
<b>Interest Calculation:</b>
Your account earns 2% interest monthly
Interest is added automatically
"""
    
    keyboard = [
        [
            InlineKeyboardButton("💰 Deposit", callback_data="bank_deposit"),
            InlineKeyboardButton("💸 Withdraw", callback_data="bank_withdraw"),
        ],
        [
            InlineKeyboardButton("📊 Transactions", callback_data="bank_transactions"),
            InlineKeyboardButton("⚙️ Settings", callback_data="bank_settings"),
        ],
    ]
    
    await update.message.reply_text(
        bank_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Bank viewed by {user_id}")

bank_handler = CommandHandler('bank', bank_command)