"""
TELEGRAM RPG BOT - ENHANCEMENTS MODULE
Contains all 4 new features in one place:
1. Display first_name/username instead of user IDs
2. Group commands with reply-to support
3. Group marriage proposals with buttons
4. Permission system for friend/adopt

Simply import and add handlers in bot.py!
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import db
from modules.utils.cooldown import CooldownManager
import random
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# UTILITY FUNCTIONS (Used everywhere)
# ============================================================================

def get_display_name(user):
    """Get display name for user - prefer first_name, then username, then fallback"""
    if user.get('first_name'):
        return user['first_name']
    elif user.get('username'):
        return f"@{user['username']}"
    else:
        return f"user{user['user_id']}"


async def get_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Extract target user from:
    1. reply_to_message.from_user (if replying to someone)
    2. context.args[0] as @username (fallback)
    
    Returns: (target_user_id, target_name, error_message)
    """
    # Check if replying to a message
    if update.message and update.message.reply_to_message:
        target_user_id = update.message.reply_to_message.from_user.id
        target_user = db.get_user(target_user_id)
        if target_user:
            target_name = get_display_name(target_user)
        else:
            target_name = (
                update.message.reply_to_message.from_user.first_name or
                update.message.reply_to_message.from_user.username or
                f"user{target_user_id}"
            )
        return target_user_id, target_name, None
    
    # Fall back to @username argument
    if not context.args:
        return None, None, "Reply to a user or use /command @username"
    
    target_username = context.args[0].lstrip('@')
    target_user = db.db.users.find_one({"username": target_username})
    
    if not target_user:
        return None, None, f"❌ User @{target_username} not found"
    
    target_user_id = target_user['user_id']
    target_name = get_display_name(target_user)
    
    return target_user_id, target_name, None


# ============================================================================
# CHANGE 1: LEADERBOARD DISPLAY WITH NAMES
# ============================================================================

async def enhanced_leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View top players with names"""
    users = db.get_leaderboard('level', 10)
    
    lb_text = "<b>🏆 TOP 10 PLAYERS</b>\n\n"
    for idx, user in enumerate(users, 1):
        display_name = get_display_name(user)
        lb_text += f"{idx}. {display_name} - Level {user['level']}\n"
    
    keyboard = [
        [
            InlineKeyboardButton("💰 Money", callback_data="lb_money"),
            InlineKeyboardButton("⭐ Level", callback_data="lb_level"),
        ],
        [
            InlineKeyboardButton("👨‍👩‍👧‍👦 Family", callback_data="lb_family"),
            InlineKeyboardButton("🏭 Factory", callback_data="lb_factory"),
        ],
    ]
    
    await update.message.reply_text(
        lb_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Leaderboard viewed by {update.effective_user.id}")


async def enhanced_moneyboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View richest players with names"""
    users = db.get_leaderboard('money', 10)
    
    lb_text = "<b>💰 RICHEST PLAYERS</b>\n\n"
    for idx, user in enumerate(users, 1):
        display_name = get_display_name(user)
        lb_text += f"{idx}. {display_name} - {user['money']:,} 💰\n"
    
    await update.message.reply_text(lb_text, parse_mode="HTML")


async def enhanced_familyboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Family leaderboard with names"""
    user_id = update.effective_user.id
    
    families = []
    for family in db.db.families.find():
        family_size = (
            len(family.get('children', [])) +
            len(family.get('parents', [])) +
            len(family.get('grandchildren', [])) +
            len(family.get('siblings', [])) +
            (1 if family.get('partner') else 0) + 1
        )
        families.append({
            'user_id': family['user_id'],
            'size': family_size
        })
    
    families.sort(key=lambda x: x['size'], reverse=True)
    
    board_text = "<b>👨‍👩‍👧‍👦 FAMILY LEADERBOARD</b>\n\n"
    
    for idx, fam in enumerate(families[:10], 1):
        user = db.get_user(fam['user_id'])
        if user:
            display_name = get_display_name(user)
            board_text += f"{idx}. {display_name} - {fam['size']} members\n"
    
    await update.message.reply_text(board_text, parse_mode="HTML")
    logger.info(f"Family board viewed by {user_id}")


async def enhanced_factoryboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Factory leaderboard with names"""
    user_id = update.effective_user.id
    
    factories = list(db.db.factory.find()
        .sort("production", -1)
        .limit(10))
    
    if not factories:
        await update.message.reply_text("❌ No factories yet")
        return
    
    board_text = "<b>🏭 FACTORY LEADERBOARD</b>\n\n"
    
    for idx, factory in enumerate(factories, 1):
        owner = db.get_user(factory['user_id'])
        if owner:
            display_name = get_display_name(owner)
            board_text += f"{idx}. {display_name}\n"
            board_text += f"   Level: {factory.get('level', 1)}\n"
            board_text += f"   Production: {factory.get('production', 0)} units\n"
            board_text += f"   Workers: {factory.get('workers', 0)}\n"
            board_text += f"   Revenue: {factory.get('money_generated', 0):,} 💰\n\n"
    
    await update.message.reply_text(board_text, parse_mode="HTML")
    logger.info(f"Factory board viewed by {user_id}")


# ============================================================================
# CHANGE 2: GROUP COMMANDS WITH REPLY-TO SUPPORT
# ============================================================================

async def enhanced_marry_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Marry command with reply-to + group proposal support"""
    user_id = update.effective_user.id
    chat = update.effective_chat
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    family = db.get_family(user_id)
    
    if family.get('partner'):
        partner = db.get_user(family['partner'])
        await update.message.reply_text(
            f"❌ You are already married to {get_display_name(partner)}\n\n"
            f"Use /divorce to end your marriage."
        )
        return
    
    target_user_id, target_name, error = await get_target_user(update, context)
    
    if error:
        if not context.args and not (update.message and update.message.reply_to_message):
            await update.message.reply_text(
                "💍 <b>MARRIAGE SYSTEM</b>\n\n"
                "Usage: /marry @username\n"
                "Or: Reply to someone's message + /marry\n\n"
                "They will receive a proposal notification.",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(f"❌ {error}")
        return
    
    target = db.get_user(target_user_id)
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target_user_id == user_id:
        await update.message.reply_text("❌ You can't marry yourself!")
        return
    
    target_family = db.get_family(target_user_id)
    if target_family.get('partner'):
        await update.message.reply_text(f"❌ {target_name} is already married")
        return
    
    proposer_name = get_display_name(user)
    
    # CHANGE 3: Determine where to send proposal
    if chat.type in ['group', 'supergroup']:
        proposal_chat_id = chat.id
        proposal_text = f"💍 <b>{proposer_name}</b> proposed to <b>{target_name}</b> in the group!"
    else:
        proposal_chat_id = target_user_id
        proposal_text = f"💍 <b>You received a marriage proposal!</b>\n\n<b>{proposer_name}</b> wants to marry you!"
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_marry_{user_id}_{target_user_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_marry_{user_id}_{target_user_id}"),
        ]
    ]
    
    try:
        await context.bot.send_message(
            chat_id=proposal_chat_id,
            text=proposal_text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Failed to send proposal: {e}")
        await update.message.reply_text("❌ Could not send proposal")
        return
    
    await update.message.reply_text(f"✅ Proposal sent to {target_name}!")
    logger.info(f"Marriage proposal: {user_id} -> {target_user_id}")


async def enhanced_adopt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adopt command with reply-to + permission system"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    family = db.get_family(user_id)
    
    if len(family.get('children', [])) >= 10:
        await update.message.reply_text("❌ You have reached the maximum children limit (10)")
        return
    
    target_user_id, target_name, error = await get_target_user(update, context)
    
    if error:
        if not context.args and not (update.message and update.message.reply_to_message):
            await update.message.reply_text(
                "👶 <b>ADOPTION</b>\n\n"
                "Usage: /adopt @username\n"
                "Or: Reply to someone's message + /adopt\n\n"
                "They will receive an adoption request for approval.",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(f"❌ {error}")
        return
    
    target = db.get_user(target_user_id)
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target_user_id == user_id:
        await update.message.reply_text("❌ You can't adopt yourself!")
        return
    
    target_family = db.get_family(target_user_id)
    if target_family.get('parents'):
        await update.message.reply_text(f"❌ {target_name} already has parents")
        return
    
    requester_name = get_display_name(user)
    
    # CHANGE 4: Send permission request
    keyboard = [
        [
            InlineKeyboardButton("��� Accept", callback_data=f"accept_adopt_{user_id}_{target_user_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_adopt_{user_id}_{target_user_id}"),
        ]
    ]
    
    try:
        await context.bot.send_message(
            chat_id=target_user_id,
            text=f"👶 <b>Adoption Request!</b>\n\n"
                 f"<b>{requester_name}</b> wants to adopt you as their child.\n\n"
                 f"Do you accept?",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Could not send adoption request: {e}")
        await update.message.reply_text(f"❌ Could not send request to {target_name}")
        return
    
    await update.message.reply_text(
        f"✅ <b>Adoption Request Sent!</b>\n\n"
        f"Waiting for {target_name}'s approval...",
        parse_mode="HTML"
    )
    
    logger.info(f"Adoption request: {user_id} -> {target_user_id}")


async def enhanced_friend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Friend command with reply-to + permission system"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Use /start first")
        return
    
    target_user_id, target_name, error = await get_target_user(update, context)
    
    if error:
        if not context.args and not (update.message and update.message.reply_to_message):
            await update.message.reply_text(
                "👥 <b>ADD FRIEND</b>\n\n"
                "Usage: /friend @username\n"
                "Or: Reply to someone's message + /friend",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(f"❌ {error}")
        return
    
    target = db.get_user(target_user_id)
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target_user_id == user_id:
        await update.message.reply_text("❌ Can't friend yourself!")
        return
    
    if target_user_id in user.get('friends', []):
        await update.message.reply_text(f"✅ Already friends with {target_name}")
        return
    
    requester_name = get_display_name(user)
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_friend_{user_id}_{target_user_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_friend_{user_id}_{target_user_id}"),
        ]
    ]
    
    try:
        await context.bot.send_message(
            chat_id=target_user_id,
            text=f"👥 <b>{requester_name}</b> wants to add you as a friend.\n\n"
                 f"Accept this request?",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Could not send friend request: {e}")
        await update.message.reply_text(f"❌ Could not send request to {target_name}")
        return
    
    await update.message.reply_text(
        f"✅ <b>Friend Request Sent!</b>\n\n"
        f"Waiting for {target_name}'s approval...",
        parse_mode="HTML"
    )
    
    logger.info(f"Friend request: {user_id} -> {target_user_id}")


async def enhanced_kill_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kill command with reply-to support"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    target_user_id, target_name, error = await get_target_user(update, context)
    
    if error:
        if not context.args and not (update.message and update.message.reply_to_message):
            await update.message.reply_text(
                "⚔️ <b>ATTACK SYSTEM</b>\n\n"
                "Usage: /kill @username\n"
                "Or: Reply to someone's message + /kill\n\n"
                "<b>⚠️ WARNING:</b>\n"
                "• Serious consequences\n"
                "• Victim loses money/items\n"
                "• You gain reputation (evil)\n"
                "• Can result in jail time",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(f"❌ {error}")
        return
    
    can_kill, remaining = CooldownManager.check_cooldown(user_id, 'kill', 7200)
    if not can_kill:
        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        await update.message.reply_text(f"⏳ You can attack again in {hours}h {minutes}m")
        return
    
    target = db.get_user(target_user_id)
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target_user_id == user_id:
        await update.message.reply_text("❌ You can't attack yourself!")
        return
    
    user_power = user['level'] * 10 + len(user.get('weapons', [])) * 5
    target_power = target['level'] * 10 + len(target.get('weapons', [])) * 5
    
    success_rate = max(10, min(90, (user_power - target_power) + 50))
    
    if random.randint(0, 100) < success_rate:
        damage = random.randint(100, 500)
        db.withdraw_money(target_user_id, damage)
        db.update_user(user_id, {'reputation': user['reputation'] + 10})
        CooldownManager.set_cooldown(user_id, 'kill')
        
        if random.randint(0, 100) < 70:
            jail_time = random.randint(2, 8)
            db.update_user(user_id, {'jail_time': jail_time})
            
            await update.message.reply_text(
                f"⚔️ <b>ATTACK SUCCESSFUL!</b>\n\n"
                f"💥 Defeated {target_name}\n"
                f"💰 Stole {damage:,} coins\n"
                f"⭐ Reputation +10\n\n"
                f"🚨 <b>BUT:</b> Police arrested you!\n"
                f"⏳ Jail time: {jail_time} hours",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(
                f"⚔️ <b>ATTACK SUCCESSFUL!</b>\n\n"
                f"💥 Defeated {target_name}\n"
                f"💰 Stole {damage:,} coins\n"
                f"⭐ Reputation +10",
                parse_mode="HTML"
            )
        logger.info(f"Attack: {user_id} attacked {target_user_id} for {damage}")
    else:
        CooldownManager.set_cooldown(user_id, 'kill')
        await update.message.reply_text(
            f"❌ <b>ATTACK FAILED!</b>\n\n"
            f"{target_name} defended successfully!\n"
            f"Try again in 2 hours."
        )


async def enhanced_rob_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rob command with reply-to support"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    target_user_id, target_name, error = await get_target_user(update, context)
    
    if error:
        if not context.args and not (update.message and update.message.reply_to_message):
            await update.message.reply_text(
                "🔫 <b>ROB SYSTEM</b>\n\n"
                "Usage: /rob @username\n"
                "Or: Reply to someone's message + /rob\n\n"
                "Steal money from another player.\n"
                "<i>Risk: You might get caught!</i>",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(f"❌ {error}")
        return
    
    can_rob, remaining = CooldownManager.check_cooldown(user_id, 'rob', 3600)
    if not can_rob:
        minutes = int(remaining // 60)
        await update.message.reply_text(f"⏳ You can rob again in {minutes}m")
        return
    
    target = db.get_user(target_user_id)
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target_user_id == user_id:
        await update.message.reply_text("❌ You can't rob yourself!")
        return
    
    if target['money'] <= 0:
        await update.message.reply_text(f"❌ {target_name} has no money to rob")
        return
    
    steal_amount = random.randint(int(target['money'] * 0.1), int(target['money'] * 0.5))
    success_rate = max(20, min(80, user['level'] * 5 - target['level'] * 5))
    
    if random.randint(0, 100) < success_rate:
        db.withdraw_money(target_user_id, steal_amount)
        db.add_money(user_id, steal_amount)
        CooldownManager.set_cooldown(user_id, 'rob')
        db.update_user(user_id, {'reputation': user['reputation'] + 5})
        
        await update.message.reply_text(
            f"✅ <b>ROB SUCCESSFUL!</b>\n\n"
            f"🏃 Stole {steal_amount:,} 💰 from {target_name}\n"
            f"Your new balance: {user['money'] + steal_amount:,} 💰",
            parse_mode="HTML"
        )
        logger.info(f"Rob: {user_id} robbed {target_user_id} for {steal_amount}")
    else:
        CooldownManager.set_cooldown(user_id, 'rob')
        
        if random.randint(0, 100) < 40:
            jail_time = random.randint(1, 6)
            db.update_user(user_id, {'jail_time': jail_time})
            
            await update.message.reply_text(
                f"❌ <b>ROB FAILED!</b>\n\n"
                f"🚨 You got caught by police!\n"
                f"⏳ Jail time: {jail_time} hours\n\n"
                f"Use /bail to get out early"
            )
        else:
            await update.message.reply_text(
                f"❌ <b>ROB FAILED!</b>\n\n"
                f"🏃 You got away, but didn't steal anything!"
            )


async def enhanced_pay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pay command with reply-to support"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    target_user_id, target_name, error = await get_target_user(update, context)
    
    if error:
        if not context.args and not (update.message and update.message.reply_to_message):
            await update.message.reply_text(
                "💳 <b>PAYMENT</b>\n\n"
                "Usage: /pay @username amount\n"
                "Or: Reply to someone's message + /pay amount\n\n"
                "Example: /pay @friend 100",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(f"❌ {error}")
        return
    
    if update.message.reply_to_message:
        if not context.args:
            await update.message.reply_text("❌ Please specify amount: /pay (replying) 100")
            return
        try:
            amount = int(context.args[0])
        except ValueError:
            await update.message.reply_text("❌ Invalid amount")
            return
    else:
        if len(context.args) < 2:
            await update.message.reply_text("💳 <b>PAYMENT</b>\n\nUsage: /pay @username amount", parse_mode="HTML")
            return
        try:
            amount = int(context.args[1])
        except ValueError:
            await update.message.reply_text("❌ Invalid amount")
            return
    
    target = db.get_user(target_user_id)
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target_user_id == user_id:
        await update.message.reply_text("❌ You can't pay yourself!")
        return
    
    if amount <= 0:
        await update.message.reply_text("❌ Amount must be positive")
        return
    
    if user['money'] < amount:
        await update.message.reply_text(f"❌ You only have {user['money']} 💰")
        return
    
    db.withdraw_money(user_id, amount)
    db.add_money(target_user_id, amount)
    
    await update.message.reply_text(
        f"✅ <b>PAYMENT SENT</b>\n\n"
        f"💳 Sent {amount:,} 💰 to {target_name}\n"
        f"Your balance: {user['money'] - amount:,} 💰",
        parse_mode="HTML"
    )
    
    logger.info(f"Payment: {user_id} paid {target_user_id} {amount}")


# ============================================================================
# CHANGE 4: PERMISSION CALLBACK HANDLER
# ============================================================================

async def permission_callback_handler_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle accept/reject for friend and adopt requests"""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split('_')
    
    if len(parts) != 4:
        await query.answer("Invalid request", show_alert=True)
        return
    
    action, request_type, requester_id_str, target_id_str = parts
    
    try:
        requester_id = int(requester_id_str)
        target_id = int(target_id_str)
    except ValueError:
        await query.answer("Invalid IDs", show_alert=True)
        return
    
    if query.from_user.id != target_id:
        await query.answer("❌ This request is not for you!", show_alert=True)
        return
    
    requester = db.get_user(requester_id)
    target = db.get_user(target_id)
    
    if not requester or not target:
        await query.answer("❌ User not found", show_alert=True)
        return
    
    requester_name = get_display_name(requester)
    target_name = get_display_name(target)
    
    if action == "accept":
        if request_type == "friend":
            db.db.users.update_one(
                {"user_id": requester_id},
                {"$addToSet": {"friends": target_id}}
            )
            db.db.users.update_one(
                {"user_id": target_id},
                {"$addToSet": {"friends": requester_id}}
            )
            
            await query.edit_message_text(
                f"✅ <b>{target_name} accepted the friend request!</b>\n\n"
                f"You are now friends with {requester_name}.",
                parse_mode="HTML"
            )
            
            try:
                await context.bot.send_message(
                    chat_id=requester_id,
                    text=f"✅ <b>Friend Request Accepted!</b>\n\n"
                         f"{target_name} accepted your friend request.\n"
                         f"You are now friends!",
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Could not notify requester: {e}")
            
            logger.info(f"Friends: {requester_id} and {target_id} are now friends")
        
        elif request_type == "adopt":
            db.add_child(requester_id, target_id)
            
            await query.edit_message_text(
                f"✅ <b>Adoption Request Accepted!</b>\n\n"
                f"You are now the child of {requester_name}.",
                parse_mode="HTML"
            )
            
            try:
                await context.bot.send_message(
                    chat_id=requester_id,
                    text=f"✅ <b>Adoption Request Accepted!</b>\n\n"
                         f"{target_name} accepted your adoption request.\n"
                         f"They are now your child!",
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Could not notify requester: {e}")
            
            logger.info(f"Adoption: {requester_id} adopted {target_id}")
    
    elif action == "reject":
        await query.edit_message_text(
            f"❌ <b>Request Rejected</b>\n\n"
            f"You declined the {request_type} request.",
            parse_mode="HTML"
        )
        
        try:
            await context.bot.send_message(
                chat_id=requester_id,
                text=f"❌ <b>Request Declined</b>\n\n"
                     f"{target_name} declined your {request_type} request.",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Could not notify requester: {e}")
        
        logger.info(f"{request_type.capitalize()} declined: {requester_id} -> {target_id}")


# ============================================================================
# MARRIAGE PROPOSAL CALLBACKS (for group proposals)
# ============================================================================

async def marriage_callback_handler_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle accept/reject for marriage proposals"""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split('_')
    
    if len(parts) != 4 or parts[0:2] != ['accept', 'marry'] and parts[0:2] != ['reject', 'marry']:
        return
    
    try:
        proposer_id = int(parts[2])
        target_id = int(parts[3])
    except ValueError:
        return
    
    if query.from_user.id != target_id:
        await query.answer("❌ This proposal is not for you!", show_alert=True)
        return
    
    proposer = db.get_user(proposer_id)
    target = db.get_user(target_id)
    
    if not proposer or not target:
        await query.answer("❌ User not found", show_alert=True)
        return
    
    action = parts[0]
    proposer_name = get_display_name(proposer)
    target_name = get_display_name(target)
    
    if action == "accept":
        db.add_partner(proposer_id, target_id)
        
        await query.edit_message_text(
            f"💍 <b>MARRIAGE ACCEPTED!</b>\n\n"
            f"{proposer_name} and {target_name} are now married!",
            parse_mode="HTML"
        )
        
        try:
            await context.bot.send_message(
                chat_id=proposer_id,
                text=f"💍 <b>Marriage Accepted!</b>\n\n"
                     f"{target_name} accepted your proposal!\n"
                     f"You are now married!",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Could not notify proposer: {e}")
        
        logger.info(f"Marriage: {proposer_id} and {target_id} are now married")
    
    elif action == "reject":
        await query.edit_message_text(
            f"💔 <b>Proposal Rejected</b>\n\n"
            f"You declined the marriage proposal.",
            parse_mode="HTML"
        )
        
        try:
            await context.bot.send_message(
                chat_id=proposer_id,
                text=f"💔 <b>Proposal Rejected</b>\n\n"
                     f"{target_name} declined your marriage proposal.",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Could not notify proposer: {e}")
        
        logger.info(f"Marriage proposal rejected: {proposer_id} -> {target_id}")


# ============================================================================
# EXPORT ALL HANDLERS
# ============================================================================

# Leaderboard handlers (REPLACE OLD ONES)
enhanced_leaderboard_handler = CommandHandler('leaderboard', enhanced_leaderboard_command)
enhanced_moneyboard_handler = CommandHandler('moneyboard', enhanced_moneyboard_command)
enhanced_familyboard_handler = CommandHandler('familyboard', enhanced_familyboard_command)
enhanced_factoryboard_handler = CommandHandler('factoryboard', enhanced_factoryboard_command)

# Enhanced commands (REPLACE OLD ONES)
enhanced_marry_handler = CommandHandler('marry', enhanced_marry_command)
enhanced_adopt_handler = CommandHandler('adopt', enhanced_adopt_command)
enhanced_friend_handler = CommandHandler('friend', enhanced_friend_command)
enhanced_kill_handler = CommandHandler('kill', enhanced_kill_command)
enhanced_rob_handler = CommandHandler('rob', enhanced_rob_command)
enhanced_pay_handler = CommandHandler('pay', enhanced_pay_command)

# Callback handlers (NEW)
permission_callback = CallbackQueryHandler(
    permission_callback_handler_func,
    pattern=r"^(accept|reject)_(friend|adopt)_\d+_\d+$"
)
marriage_proposal_callback = CallbackQueryHandler(
    marriage_callback_handler_func,
    pattern=r"^(accept|reject)_marry_\d+_\d+$"
)
