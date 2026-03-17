"""
/bail command - Pay bail to get out of jail
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def bail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pay bail"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    jail_time = user.get('jail_time', 0)
    
    if jail_time <= 0:
        await update.message.reply_text("✅ You are not in jail")
        return
    
    bail_cost = jail_time * 50
    
    if not context.args:
        await update.message.reply_text(
            f"⚖️ <b>BAIL</b>\n\n"
            f"⏳ Jail time: {jail_time} hours\n"
            f"💰 Bail cost: {bail_cost} coins\n\n"
            f"Usage: /bail confirm",
            parse_mode="HTML"
        )
        return
    
    if context.args[0].lower() != 'confirm':
        await update.message.reply_text("❌ Invalid command. Use /bail confirm")
        return
    
    if user['money'] < bail_cost:
        await update.message.reply_text(f"❌ You need {bail_cost} 💰")
        return
    
    # Pay bail
    db.withdraw_money(user_id, bail_cost)
    db.update_user(user_id, {'jail_time': 0})
    
    await update.message.reply_text(
        f"✅ <b>BAIL PAID</b>\n\n"
        f"💰 Paid {bail_cost} coins\n"
        f"🚔 You are free!",
        parse_mode="HTML"
    )
    logger.info(f"Bail: {user_id} paid {bail_cost} to get out of jail")

bail_handler = CommandHandler('bail', bail_command)