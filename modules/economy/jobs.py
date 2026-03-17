"""
/job and /work commands - Job system
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
from modules.utils.cooldown import CooldownManager
import random
import logging

logger = logging.getLogger(__name__)

JOBS = {
    "farmer": {"pay": 50, "emoji": "🌾"},
    "worker": {"pay": 75, "emoji": "👷"},
    "trader": {"pay": 100, "emoji": "🏪"},
    "guard": {"pay": 120, "emoji": "🛡️"},
    "scientist": {"pay": 150, "emoji": "🔬"},
}

async def job_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View job info"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    current_job = user.get('job')
    
    job_text = "<b>💼 JOBS</b>\n\n"
    
    if current_job:
        job_text += f"<b>Current Job:</b> {current_job}\n\n"
    
    job_text += "<b>Available Jobs:</b>\n"
    for job_name, job_info in JOBS.items():
        job_text += f"{job_info['emoji']} {job_name.capitalize()} - {job_info['pay']} 💰/work\n"
    
    keyboard = [
        [InlineKeyboardButton(f"{job_info['emoji']} {job_name}", callback_data=f"job_select_{job_name}")]
        for job_name, job_info in JOBS.items()
    ]
    
    await update.message.reply_text(
        job_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def work_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Work at job"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not user.get('job'):
        await update.message.reply_text("❌ You don't have a job. Use /job to apply.")
        return
    
    # Check cooldown
    can_work, remaining = CooldownManager.check_cooldown(user_id, 'work', 1800)
    
    if not can_work:
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        await update.message.reply_text(f"⏳ You can work again in {minutes}m {seconds}s")
        return
    
    job_info = JOBS.get(user['job'].lower())
    if not job_info:
        await update.message.reply_text("❌ Invalid job")
        return
    
    pay = job_info['pay'] + random.randint(0, 30)
    
    db.add_money(user_id, pay)
    CooldownManager.set_cooldown(user_id, 'work')
    
    await update.message.reply_text(
        f"✅ <b>WORK COMPLETE</b>\n\n"
        f"{job_info['emoji']} {user['job']}\n"
        f"💰 +{pay} coins\n"
        f"New balance: {user['money'] + pay:,} 💰",
        parse_mode="HTML"
    )
    logger.info(f"Work completed by {user_id}: +{pay} coins")

job_handler = CommandHandler('job', job_command)
work_handler = CommandHandler('work', work_command)