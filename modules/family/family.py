"""
/family command - View family information
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def family_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View family info"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    family = db.get_family(user_id)
    
    family_text = f"""
<b>👨‍👩‍👧‍👦 FAMILY INFORMATION</b>

<b>Partner:</b> {("✅ Married" if family.get('partner') else "❌ Single")}
<b>Children:</b> {len(family.get('children', []))} / 10
<b>Parents:</b> {len(family.get('parents', []))}
<b>Grandchildren:</b> {len(family.get('grandchildren', []))}

<b>Total Family Members:</b> {len(family.get('children', [])) + len(family.get('parents', [])) + len(family.get('grandchildren', [])) + (1 if family.get('partner') else 0) + 1}

<b>Actions:</b>
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔗 Marriage", callback_data="family_marry"),
            InlineKeyboardButton("👶 Adopt", callback_data="family_adopt"),
        ],
        [
            InlineKeyboardButton("👨‍👩‍👧‍👦 Tree", callback_data="view_tree"),
            InlineKeyboardButton("📋 Full Tree", callback_data="view_fulltree"),
        ],
    ]
    
    await update.message.reply_text(
        family_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Family viewed by {user_id}")

family_handler = CommandHandler('family', family_command)