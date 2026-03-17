"""
/profile command handler
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View profile"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    family = db.get_family(user_id)
    
    profile_text = f"""
<b>👤 PROFILE</b>

<b>Username:</b> @{user['username']}
<b>Level:</b> {user['level']}
<b>Experience:</b> {user['experience']} XP

<b>💰 ECONOMY</b>
<b>Cash:</b> {user['money']:,} 💰
<b>Bank:</b> {user['bank']:,} 💰
<b>Total:</b> {(user['money'] + user['bank']):,} 💰

<b>👨‍👩‍👧‍👦 FAMILY</b>
<b>Partner:</b> {("Yes" if family.get('partner') else "None")}
<b>Children:</b> {len(family.get('children', []))}
<b>Parents:</b> {len(family.get('parents', []))}

<b>📊 STATS</b>
<b>Job:</b> {user.get('job') or 'Unemployed'}
<b>Reputation:</b> {user['reputation']}
<b>Jail Time:</b> {user.get('jail_time', 0)} hours
"""
    
    await update.message.reply_text(profile_text, parse_mode="HTML")
    logger.info(f"Profile viewed by {user_id}")

profile_handler = CommandHandler('profile', profile)