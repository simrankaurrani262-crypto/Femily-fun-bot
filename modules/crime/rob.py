"""
/rob command - Rob another player
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
from modules.utils.cooldown import CooldownManager
import random
import logging

logger = logging.getLogger(__name__)

async def rob_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rob another player"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🔫 <b>ROB SYSTEM</b>\n\n"
            "Usage: /rob @username\n\n"
            "Steal money from another player.\n"
            "<i>Risk: You might get caught!</i>",
            parse_mode="HTML"
        )
        return
    
    # Check cooldown
    can_rob, remaining = CooldownManager.check_cooldown(user_id, 'rob', 3600)
    if not can_rob:
        minutes = int(remaining // 60)
        await update.message.reply_text(f"⏳ You can rob again in {minutes}m")
        return
    
    target_username = context.args[0].lstrip('@')
    target = db.db.users.find_one({"username": target_username})
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target['user_id'] == user_id:
        await update.message.reply_text("❌ You can't rob yourself!")
        return
    
    if target['money'] <= 0:
        await update.message.reply_text(f"❌ @{target['username']} has no money to rob")
        return
    
    # Rob calculation
    steal_amount = random.randint(int(target['money'] * 0.1), int(target['money'] * 0.5))
    success_rate = max(20, min(80, user['level'] * 5 - target['level'] * 5))
    
    if random.randint(0, 100) < success_rate:
        # Success
        db.withdraw_money(target['user_id'], steal_amount)
        db.add_money(user_id, steal_amount)
        CooldownManager.set_cooldown(user_id, 'rob')
        
        db.update_user(user_id, {'reputation': user['reputation'] + 5})
        
        await update.message.reply_text(
            f"✅ <b>ROB SUCCESSFUL!</b>\n\n"
            f"🏃 Stole {steal_amount:,} 💰 from @{target['username']}\n"
            f"Your new balance: {user['money'] + steal_amount:,} 💰",
            parse_mode="HTML"
        )
        logger.info(f"Rob: {user_id} robbed {target['user_id']} for {steal_amount}")
    else:
        # Failed - might go to jail
        CooldownManager.set_cooldown(user_id, 'rob')
        
        if random.randint(0, 100) < 40:
            # Caught - go to jail
            jail_time = random.randint(1, 6)
            db.update_user(user_id, {'jail_time': jail_time})
            
            await update.message.reply_text(
                f"❌ <b>ROB FAILED!</b>\n\n"
                f"🚨 You got caught by police!\n"
                f"⏳ Jail time: {jail_time} hours\n\n"
                f"Use /bail to get out early"
            )
            logger.info(f"Jail: {user_id} jailed for {jail_time}h")
        else:
            await update.message.reply_text(
                f"❌ <b>ROB FAILED!</b>\n\n"
                f"@{target['username']} caught you!\n"
                f"💰 Lost {random.randint(10, 100)} coins as fine"
            )

rob_handler = CommandHandler('rob', rob_command)