"""
/kill command - Attack another player (with consequences)
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
from modules.utils.cooldown import CooldownManager
import random
import logging

logger = logging.getLogger(__name__)

async def kill_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Attack another player"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "⚔️ <b>ATTACK SYSTEM</b>\n\n"
            "Usage: /kill @username\n\n"
            "<b>⚠️ WARNING:</b>\n"
            "• Serious consequences\n"
            "• Victim loses money/items\n"
            "• You gain reputation (evil)\n"
            "• Can result in jail time",
            parse_mode="HTML"
        )
        return
    
    # Check cooldown
    can_kill, remaining = CooldownManager.check_cooldown(user_id, 'kill', 7200)
    if not can_kill:
        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        await update.message.reply_text(f"⏳ You can attack again in {hours}h {minutes}m")
        return
    
    target_username = context.args[0].lstrip('@')
    target = db.db.users.find_one({"username": target_username})
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target['user_id'] == user_id:
        await update.message.reply_text("❌ You can't attack yourself!")
        return
    
    # Attack calculation
    user_power = user['level'] * 10 + len(user.get('weapons', [])) * 5
    target_power = target['level'] * 10 + len(target.get('weapons', [])) * 5
    
    success_rate = max(10, min(90, (user_power - target_power) + 50))
    
    if random.randint(0, 100) < success_rate:
        # Attack successful
        damage = random.randint(100, 500)
        db.withdraw_money(target['user_id'], damage)
        db.update_user(user_id, {'reputation': user['reputation'] + 10})
        CooldownManager.set_cooldown(user_id, 'kill')
        
        # Chance to go to jail
        if random.randint(0, 100) < 70:
            jail_time = random.randint(2, 8)
            db.update_user(user_id, {'jail_time': jail_time})
            
            await update.message.reply_text(
                f"⚔️ <b>ATTACK SUCCESSFUL!</b>\n\n"
                f"💥 Defeated @{target['username']}\n"
                f"💰 Stole {damage:,} coins\n"
                f"⭐ Reputation +10\n\n"
                f"🚨 <b>BUT:</b> Police arrested you!\n"
                f"⏳ Jail time: {jail_time} hours",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(
                f"⚔️ <b>ATTACK SUCCESSFUL!</b>\n\n"
                f"💥 Defeated @{target['username']}\n"
                f"💰 Stole {damage:,} coins\n"
                f"⭐ Reputation +10",
                parse_mode="HTML"
            )
        logger.info(f"Attack: {user_id} attacked {target['user_id']} for {damage}")
    else:
        # Attack failed
        CooldownManager.set_cooldown(user_id, 'kill')
        
        counterattack_damage = random.randint(50, 200)
        db.withdraw_money(user_id, counterattack_damage)
        
        await update.message.reply_text(
            f"❌ <b>ATTACK FAILED!</b>\n\n"
            f"@{target['username']} fought back!\n"
            f"💥 You took {counterattack_damage} damage\n"
            f"💰 Lost {counterattack_damage} coins"
        )

kill_handler = CommandHandler('kill', kill_command)