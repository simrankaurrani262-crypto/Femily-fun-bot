"""
/fertilise command - Fertilise plots
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def fertilise_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fertilise a plot"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "✨ <b>FERTILISE</b>\n\n"
            "Usage: /fertilise plot_number\n"
            "Cost: 50 💰\n"
            "Effect: +25% growth speed",
            parse_mode="HTML"
        )
        return
    
    try:
        plot_num = int(context.args[0]) - 1
    except ValueError:
        await update.message.reply_text("❌ Invalid plot number")
        return
    
    garden = user.get('garden', {})
    plots = garden.get('plots', [])
    
    if plot_num < 0 or plot_num >= len(plots):
        await update.message.reply_text("❌ Plot not found")
        return
    
    fertilize_cost = 50
    
    if user['money'] < fertilize_cost:
        await update.message.reply_text(f"❌ You need {fertilize_cost} 💰")
        return
    
    # Fertilise
    db.withdraw_money(user_id, fertilize_cost)
    plots[plot_num]['growth'] = min(100, plots[plot_num].get('growth', 0) + 25)
    db.update_user(user_id, {'garden.plots': plots})
    
    await update.message.reply_text(
        f"✅ <b>PLOT FERTILISED!</b>\n\n"
        f"Plot {plot_num + 1}: {plots[plot_num]['crop']}\n"
        f"Growth: {plots[plot_num]['growth']}%\n"
        f"Cost: {fertilize_cost} 💰",
        parse_mode="HTML"
    )

fertilise_handler = CommandHandler('fertilise', fertilise_command)