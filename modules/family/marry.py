"""
/marry command - Marry someone (with reply-to support)
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
from modules.utils.group_handler import get_target_user, get_display_name
import logging

logger = logging.getLogger(__name__)

async def marry_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Marry command"""
    user_id = update.effective_user.id
    
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
    
    # Get target user (supports reply-to AND @username)
    target_user_id, target_name, error = await get_target_user(update, context)
    
    if error:
        if not context.args and not update.message.reply_to_message:
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
    
    # Create marriage
    db.add_partner(user_id, target_user_id)
    
    proposer_name = get_display_name(user)
    
    await update.message.reply_text(
        f"💍 <b>CONGRATULATIONS!</b>\n\n"
        f"You are now married to {target_name}!\n\n"
        f"View your family tree with /tree",
        parse_mode="HTML"
    )
    
    logger.info(f"Marriage: {user_id} married {target_user_id}")

marry_handler = CommandHandler('marry', marry_command)
