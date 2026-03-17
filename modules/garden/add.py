"""
/add command - Add more plots to garden
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

PLOT_COST = 500
MAX_PLOTS = 20

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add garden plot"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    garden = user.get('garden', {})
    plots = garden.get('plots', [])
    
    if len(plots) >= MAX_PLOTS:
        await update.message.reply_text(f"❌ Maximum plots ({MAX_PLOTS}) reached")
        return
    
    if not context.args or context.args[0].lower() != 'confirm':
        await update.message.reply_text(
            f"🌾 <b>ADD PLOT</b>\n\n"
            f"Current plots: {len(plots)}/{MAX_PLOTS}\n"
            f"Cost: {PLOT_COST} 💰\n\n"
            f"Usage: /add confirm",
            parse_mode="HTML"
        )
        return
    
    if user['money'] < PLOT_COST:
        await update.message.reply_text(f"❌ You need {PLOT_COST} 💰")
        return
    
    # Add plot
    db.withdraw_money(user_id, PLOT_COST)
    plots.append({
        "crop": "Empty",
        "growth": 0,
        "planted_at": None
    })
    db.update_user(user_id, {'garden.plots': plots})
    
    await update.message.reply_text(
        f"✅ <b>PLOT ADDED!</b>\n\n"
        f"Total plots: {len(plots)}/{MAX_PLOTS}\n"
        f"Cost: {PLOT_COST} 💰",
        parse_mode="HTML"
    )
    logger.info(f"Plot added: {user_id} now has {len(plots)} plots")

add_handler = CommandHandler('add', add_command)