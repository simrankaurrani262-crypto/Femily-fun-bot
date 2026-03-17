"""
/nation command - Nation building game
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def nation_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Nation game"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    nation = db.db.market.find_one({"user_id": user_id, "type": "nation"})
    
    if not nation:
        db.db.market.insert_one({
            "user_id": user_id,
            "type": "nation",
            "population": 100,
            "happiness": 50,
            "money": 1000,
            "resources": 100
        })
        nation = db.db.market.find_one({"user_id": user_id, "type": "nation"})
    
    nation_text = f"""
<b>🏛️ YOUR NATION</b>

<b>Population:</b> {nation['population']}
<b>Happiness:</b> {nation['happiness']}%
<b>Treasury:</b> {nation['money']:,} 💰
<b>Resources:</b> {nation['resources']}

Ruler: @{user['username']}
"""
    
    await update.message.reply_text(nation_text, parse_mode="HTML")

nation_handler = CommandHandler('nation', nation_command)