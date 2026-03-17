"""
/loan and /repay commands - Loan system
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

LOAN_INTEREST = 0.10  # 10% interest

async def loan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Take a loan"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "💳 <b>LOAN SYSTEM</b>\n\n"
            "Usage: /loan amount\n\n"
            f"Interest Rate: {LOAN_INTEREST * 100}%\n"
            "Maximum Loan: 10,000 💰\n\n"
            "Example: /loan 5000",
            parse_mode="HTML"
        )
        return
    
    try:
        amount = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid amount")
        return
    
    if amount <= 0:
        await update.message.reply_text("❌ Loan amount must be positive")
        return
    
    if amount > 10000:
        await update.message.reply_text("❌ Maximum loan is 10,000 💰")
        return
    
    # Check existing loan
    existing_loan = db.db.economy.find_one({"user_id": user_id, "type": "loan"})
    if existing_loan and existing_loan.get('amount', 0) > 0:
        await update.message.reply_text(
            f"❌ You already have a loan: {existing_loan['amount']} 💰\n"
            f"Repay with /repay amount"
        )
        return
    
    # Grant loan
    interest_amount = int(amount * LOAN_INTEREST)
    total_owed = amount + interest_amount
    
    db.add_money(user_id, amount)
    
    # Store loan info
    db.db.economy.update_one(
        {"user_id": user_id},
        {"$set": {
            "type": "loan",
            "amount": amount,
            "interest": interest_amount,
            "total_owed": total_owed,
            "taken_at": db.db.time.time() if hasattr(db.db, 'time') else 0
        }},
        upsert=True
    )
    
    await update.message.reply_text(
        f"✅ <b>LOAN GRANTED!</b>\n\n"
        f"💰 Loan Amount: {amount:,} 💰\n"
        f"📊 Interest (10%): {interest_amount:,} 💰\n"
        f"💳 Total to Repay: {total_owed:,} 💰\n\n"
        f"Use /repay amount to repay your loan",
        parse_mode="HTML"
    )
    logger.info(f"Loan: {user_id} took loan of {amount}")

async def repay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Repay loan"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    loan = db.db.economy.find_one({"user_id": user_id, "type": "loan"})
    
    if not loan or loan.get('amount', 0) == 0:
        await update.message.reply_text("❌ You don't have any loan")
        return
    
    if not context.args:
        await update.message.reply_text(
            f"💳 <b>REPAY LOAN</b>\n\n"
            f"Current Debt: {loan['total_owed']:,} 💰\n\n"
            f"Usage: /repay amount",
            parse_mode="HTML"
        )
        return
    
    try:
        repay_amount = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid amount")
        return
    
    if repay_amount <= 0:
        await update.message.reply_text("❌ Repay amount must be positive")
        return
    
    if user['money'] < repay_amount:
        await update.message.reply_text(f"❌ You only have {user['money']} 💰")
        return
    
    # Repay loan
    new_owed = loan['total_owed'] - repay_amount
    
    if new_owed <= 0:
        # Loan paid off
        db.withdraw_money(user_id, repay_amount)
        db.db.economy.update_one(
            {"user_id": user_id},
            {"$set": {"amount": 0, "total_owed": 0}}
        )
        
        await update.message.reply_text(
            f"✅ <b>LOAN REPAID!</b>\n\n"
            f"💰 Paid: {repay_amount:,} 💰\n"
            f"Your loan is now CLEARED!",
            parse_mode="HTML"
        )
        logger.info(f"Loan repaid: {user_id} fully repaid loan")
    else:
        db.withdraw_money(user_id, repay_amount)
        db.db.economy.update_one(
            {"user_id": user_id},
            {"$set": {"total_owed": new_owed}}
        )
        
        await update.message.reply_text(
            f"✅ <b>PAYMENT RECEIVED</b>\n\n"
            f"💰 Paid: {repay_amount:,} 💰\n"
            f"Remaining Debt: {new_owed:,} 💰",
            parse_mode="HTML"
        )
        logger.info(f"Loan payment: {user_id} paid {repay_amount}")

loan_handler = CommandHandler('loan', loan_command)
repay_handler = CommandHandler('repay', repay_command)