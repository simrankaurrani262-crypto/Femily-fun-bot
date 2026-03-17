"""
/stats command handler
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View statistics"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    family = db.get_family(user_id)
    total_money = user['money'] + user['bank']
    rank = db.get_user_rank(user_id, 'money')
    
    stats_text = f"""
<b>📊 YOUR STATISTICS</b>

<b>Level:</b> {user['level']}
<b>Experience:</b> {user['experience']} / {user['level'] * 100} XP
<b>Rank:</b> #{rank} (Money)

<b>💰 Economy</b>
<b>Wallet:</b> {user['money']:,} 💰
<b>Bank:</b> {user['bank']:,} 💰
<b>Total Wealth:</b> {total_money:,} 💰

<b>⚔️ Combat Stats</b>
<b>Reputation:</b> {user['reputation']}
<b>Jail Time:</b> {user.get('jail_time', 0)} hours

<b>👨‍👩‍👧‍👦 Family</b>
<b>Children:</b> {len(family.get('children', []))}
<b>Friends:</b> {len(user.get('friends', []))}

<b>🎮 Progress</b>
<b>Job:</b> {user.get('job') or 'Unemployed'}
"""
    
    await update.message.reply_text(stats_text, parse_mode="HTML")
    logger.info(f"Stats viewed by {user_id}")

stats_handler = CommandHandler('stats', stats_command)